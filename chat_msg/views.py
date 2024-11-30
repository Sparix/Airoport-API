from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from chat_msg.models import ChatSupport, ChatMessage
from chat_msg.serializers import (
    ChatSupportSerializer,
    ChatSupportSerializerRetrieve,
    ChatMessageSerializerCreate
)


class ChatSupportViewSet(viewsets.ModelViewSet):
    queryset = ChatSupport.objects.select_related(
        "author_created").prefetch_related("user_list", "chatmessage_set__user").filter(enabled=True)
    serializer_class = ChatSupportSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                user_list=self.request.user.id
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ChatSupportSerializerRetrieve

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author_created=self.request.user, user_list=self.request.user.id)



