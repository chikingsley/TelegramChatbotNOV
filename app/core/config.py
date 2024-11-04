from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Required fields
    BASE_URL: str
    ANTHROPIC_API_KEY: str
    ENVIRONMENT: str
    DATABASE_URL: str
    REDIS_URL: str
    NOTION_API_KEY: str
    NOTION_DATABASE_ID: str
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    NGROK_AUTHTOKEN: str
    
    # Optional fields with defaults
    LOG_LEVEL: str = "INFO"
    MAX_RETRIES: int = 3
    WEBHOOK_SECRET: str = "your-webhook-secret"
    TEST_MODE: bool = False

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 