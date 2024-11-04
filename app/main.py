from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder
import logging
from app.core.config import settings
from app.bot.handler import MessageHandler
from openai import OpenAI
from app.utils.setup_webhook import setup_webhook

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
    """Initialize bot and webhook on startup"""
    try:
        # Initialize bot
        app.state.bot = (
            ApplicationBuilder()
            .token(settings.TELEGRAM_BOT_TOKEN)
            .build()
            .bot
        )
        logger.info("Bot initialized")
        
        # Set up webhook
        if setup_webhook():
            logger.info("Webhook setup completed")
        else:
            logger.error("Failed to set up webhook")
            
    except Exception as e:
        logger.error(f"Startup error: {e}") 