# Project Structure
chatbot/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handler.py    # Telegram message handler
│   │   └── utils.py      # Helper functions
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py     # Configuration settings
│   │
│   └── services/
│       ├── __init__.py
│       └── openai_service.py  # OpenAI integration
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md

# Key Files:

## docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

## docker/docker-compose.yml
version: '3.8'

services:
  bot:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    volumes:
      - ..:/app
    env_file:
      - ../.env

## requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
python-telegram-bot==20.6
openai==1.3.5
python-dotenv==1.0.0
pyngrok==7.0.1
httpx==0.25.2

## .env.example
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
ENVIRONMENT=development
LOG_LEVEL=INFO

## app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()

## app/main.py
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder
import logging
from app.core.config import settings
from app.bot.handler import MessageHandler
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(request: Request):
    """Handle incoming Telegram webhook requests"""
    try:
        data = await request.json()
        update = Update.de_json(data, app.state.bot)
        
        if update.message and update.message.text:
            handler = MessageHandler(app.state.bot, openai_client)
            await handler.handle_message(update.message)
            
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

@app.on_event("startup")
async def startup_event():
    """Initialize bot on startup"""
    app.state.bot = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .build()
        .bot
    )
    logger.info("Bot initialized")

## app/bot/handler.py
from telegram import Update, Message
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self, bot, openai_client: OpenAI):
        self.bot = bot
        self.openai_client = openai_client
        self.conversation_history = {}  # Store conversation history per user

    async def handle_message(self, message: Message):
        """Handle incoming messages"""
        chat_id = message.chat_id
        user_message = message.text

        try:
            # Get conversation history for this user
            history = self.conversation_history.get(chat_id, [])
            
            # Add user message to history
            history.append({"role": "user", "content": user_message})
            
            # Get OpenAI response
            response = await self._get_ai_response(history)
            
            # Add AI response to history
            history.append({"role": "assistant", "content": response})
            
            # Update conversation history (keep last 10 messages)
            self.conversation_history[chat_id] = history[-10:]
            
            # Send response to user
            await self.bot.send_message(
                chat_id=chat_id,
                text=response
            )
            
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await self.bot.send_message(
                chat_id=chat_id,
                text="Sorry, I encountered an error. Please try again."
            )

    async def _get_ai_response(self, conversation_history):
        """Get response from OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=conversation_history,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

## app/services/openai_service.py
from openai import OpenAI
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, client: OpenAI):
        self.client = client

    async def get_response(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500
    ) -> str:
        """
        Get a response from OpenAI's API
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise

# Setup and Usage Instructions:

1. Clone the repository and set up the environment:
```bash
# Clone the repository
git clone <your-repo>
cd chatbot

# Create and activate virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

3. Run with Docker:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

4. Set up ngrok for development:
```bash
# In a new terminal
ngrok http 8000
```

5. Set the Telegram webhook:
```bash
curl -F "url=https://your-ngrok-url/webhook" https://api.telegram.org/bot<your-bot-token>/setWebhook
```

6. Start chatting with your bot on Telegram!

# Adding New Tools:
To add new tools/integrations:

1. Create a new service in app/services/
2. Add configuration in app/core/config.py
3. Update the MessageHandler to use the new service
4. Add any new environment variables to .env.example

# Error Handling:
- All exceptions are caught and logged
- Users receive friendly error messages
- Detailed logs help with debugging

# Security Notes:
- API keys are stored in environment variables
- Webhook URL should use HTTPS
- Keep conversation history in memory (add database for persistence if needed)

The project uses FastAPI for the web server, python-telegram-bot for Telegram integration, and the OpenAI API for chat completions. The Docker setup ensures consistent development and deployment environments.