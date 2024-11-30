"""
ASGI config for Airport_API project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from chat_msg.jwt_middleware import JWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Airport_API.settings")

asgi_app = get_asgi_application()

from chat_msg import routing

application = ProtocolTypeRouter({
    "http": asgi_app,
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(
                routing.websocket_urlpatterns
        )
    ))
})
