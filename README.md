# Telegram AI Chatbot

A Docker-based Telegram chatbot using OpenAI's GPT models.

## Setup

1. Clone the repository:```bash
git clone <repository-url>
cd chatbot
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Build and run with Docker:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Development

- The bot uses FastAPI for the webhook server
- OpenAI's GPT-4 for responses
- ngrok for tunnel creation
- Docker for containerization

## Structure

```
chatbot/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── app/
│   ├── main.py
│   ├── bot/
│   │   └── handler.py
│   ├── core/
│   │   └── config.py
│   └── utils/
│       └── setup_webhook.py
│
├── requirements.txt
├── .env
└── README.md
```

## Environment Variables

Required environment variables:
- TELEGRAM_BOT_TOKEN
- OPENAI_API_KEY
- NGROK_AUTHTOKEN

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 
