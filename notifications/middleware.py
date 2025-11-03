import logging
import jwt
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


logger = logging.getLogger("notifications")
User = get_user_model()

@database_sync_to_async
def get_user_from_payload(payload):
    try:
        user_id = payload.get("user_id")
        user = User.objects.get(id=user_id)
        logger.info(f"Found user: {user}")
        return user
    except User.DoesNotExist:
        logger.warning(f"User not found for payload: {payload}")
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope.get("query_string", b"").decode())
        token_list = query_string.get("token")
        if token_list:
            token = token_list[0]
            logger.info(f"Received JWT token: {token}")
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                logger.info(f"JWT payload: {payload}")
                scope["user"] = await get_user_from_payload(payload)
            except jwt.ExpiredSignatureError:
                logger.warning("JWT expired")
                scope["user"] = AnonymousUser()
            except jwt.InvalidTokenError as e:
                logger.warning(f"JWT invalid: {e}")
                scope["user"] = AnonymousUser()
        else:
            logger.warning("No JWT token provided in query string")
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
