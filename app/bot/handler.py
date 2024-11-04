from telegram import Update, Message
from openai import OpenAI
import logging
from typing import Dict, List
import json

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self, bot, openai_client: OpenAI):
        self.bot = bot
        self.openai_client = openai_client
        self.conversation_history: Dict[int, List[Dict]] = {}
        
        # System message to set the AI's behavior
        self.system_message = {
            "role": "system",
            "content": """You are a helpful AI assistant. 
            Be concise but friendly in your responses.
            If you're not sure about something, say so.
            If asked about your capabilities, explain what you can do."""
        }

    async def handle_message(self, message: Message):
        """Handle incoming messages"""
        chat_id = message.chat_id
        user_message = message.text

        try:
            # Initialize conversation history if it doesn't exist
            if chat_id not in self.conversation_history:
                self.conversation_history[chat_id] = [self.system_message]
            
            # Add user message to history
            self.conversation_history[chat_id].append({
                "role": "user",
                "content": user_message
            })
            
            # Get OpenAI response
            response = await self._get_ai_response(chat_id)
            
            # Add AI response to history
            self.conversation_history[chat_id].append({
                "role": "assistant",
                "content": response
            })
            
            # Trim history if it gets too long (keep last 10 messages)
            if len(self.conversation_history[chat_id]) > 12:  # 10 + system message + buffer
                self.conversation_history[chat_id] = [
                    self.system_message,
                    *self.conversation_history[chat_id][-10:]
                ]
            
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

    async def _get_ai_response(self, chat_id: int) -> str:
        """Get response from OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-1106-preview",  # You can change this to gpt-3.5-turbo for lower costs
                messages=self.conversation_history[chat_id],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise 