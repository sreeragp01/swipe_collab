import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application early to populate AppRegistry
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from chat.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})