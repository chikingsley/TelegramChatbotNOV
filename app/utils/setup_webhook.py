import requests
import os
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_ngrok_url():
    """Get the public URL from ngrok"""
    try:
        # Connect to ngrok API
        response = requests.get("http://ngrok:4040/api/tunnels")
        data = response.json()
        
        # Extract the HTTPS URL
        url = next(
            tunnel["public_url"]
            for tunnel in data["tunnels"]
            if tunnel["proto"] == "https"
        )
        return url
    except Exception as e:
        logger.error(f"Failed to get ngrok URL: {e}")
        return None

def setup_webhook():
    """Set up the Telegram webhook"""
    try:
        # Wait for ngrok to be ready
        import time
        time.sleep(5)
        
        # Get the ngrok URL
        ngrok_url = get_ngrok_url()
        if not ngrok_url:
            logger.error("Failed to get ngrok URL")
            return False
            
        # Set up the webhook
        webhook_url = f"{ngrok_url}/webhook"
        api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
        
        response = requests.post(
            api_url,
            json={"url": webhook_url}
        )
        
        if response.status_code == 200 and response.json().get("ok"):
            logger.info(f"Webhook set up successfully at {webhook_url}")
            return True
        else:
            logger.error(f"Failed to set webhook: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error setting up webhook: {e}")
        return False

if __name__ == "__main__":
    setup_webhook() 