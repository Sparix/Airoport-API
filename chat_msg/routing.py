from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('api/chat/<str:room_name>/', consumers.ChatConsumer),
]