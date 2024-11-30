from django.urls import path, include
from rest_framework import routers

from chat_msg.views import ChatSupportViewSet

router = routers.DefaultRouter()
router.register("chat", ChatSupportViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "chat_msg"