import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from django.contrib.auth import get_user_model
from .models import ChatSession, Message
import httpx
import logging

from asgiref.sync import sync_to_async

logger = logging.getLogger(__name__)

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        logger.info(f"Connecting user: {user}")
        if user.is_anonymous:
            logger.warning("Anonymous user attempted to connect")
            raise DenyConnection("Authentication failed")

        if hasattr(user, "_wrapped"):
            user = user._wrapped

        self.group_name = f"notifications"

        # Join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            logger.info(f"Disconnecting from group: {self.group_name}")
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        # For notifications, we might not expect to receive messages from clients
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "notification": event["message"]
        }))

class ChatBotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        logger.info(f"Connecting user: {user}")
        if user.is_anonymous:
            logger.warning("Anonymous user attempted to connect")
            raise DenyConnection("Authentication failed")

        if hasattr(user, "_wrapped"):
            user = user._wrapped

        # Get session_id or generate new one
        self.session_id = self.scope['url_route']['kwargs'].get('session_id')
        if not self.session_id:
            self.session_id = str(uuid.uuid4())

        self.group_name = f"chat_{self.session_id}"

        # Get or create chat session
        self.chat_session, _ = await self.get_or_create_chat_session(user)

        # Join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Send session ID and history
        history = await self.get_chat_history()
        await self.send(text_data=json.dumps({
            "message": f"Connected to chat session {self.session_id}",
            "session_id": self.session_id,
            "history": history
        }))

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        logger.info(f"Received message: {text_data}")
        data = json.loads(text_data)
        user_message = data.get("message")
        logger.info(f"User message: {user_message}")
        if not user_message:
            return

        # Save user message
        await self.save_message("user", user_message)

        # Call AI API
        bot_response = await self.call_ai_api(user_message)

        # Save bot response
        await self.save_message("bot", bot_response)

        # Send response
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": bot_response
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))

    # ---------- Helper Methods ----------

    @database_sync_to_async
    def get_or_create_chat_session(self, user):
        return ChatSession.objects.get_or_create(session_id=self.session_id, user=user)

    @database_sync_to_async
    def save_message(self, sender, content):
        return Message.objects.create(chat_session=self.chat_session, sender=sender, content=content)

    async def get_chat_history(self):
        # Wrap ORM call with sync_to_async
        messages = await sync_to_async(list)(
            Message.objects.filter(chat_session=self.chat_session)
            .order_by('timestamp')
            .values('sender', 'content', 'timestamp')
        )

        # Convert datetime to string
        history = []
        for msg in messages:
            history.append({
                "sender": msg["sender"],
                "content": msg["content"],
                "timestamp": msg["timestamp"].isoformat()
            })
        return history


    async def call_ai_api(self, user_message):
        """
        Calls OpenAI Responses API (gpt-4.1) and returns the generated text.
        """
        return f"Error contacting AI API: No Chat bot"
