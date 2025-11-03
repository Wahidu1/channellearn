# channellearn/asgi.py
import os
from django.core.asgi import get_asgi_application

# 1. SET DJANGO SETTINGS FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'channellearn.settings')

# 2. CALL django.setup() — THIS IS REQUIRED!
import django
django.setup()
from notifications.middleware import JWTAuthMiddleware

# 3. NOW import routing (which imports models, consumers, etc.)
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import notifications.routing  # ← NOW SAFE!

# 4. Define application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})
