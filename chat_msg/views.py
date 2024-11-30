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


    @action(detail=True, methods=["POST"], serializer_class=ChatMessageSerializerCreate)
    def create_message(self, request, pk=None):

        data = request.data.copy()
        data["support_msg"] = pk

        serializer = ChatMessageSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["PUT"],
            serializer_class=ChatMessageSerializerCreate,
            url_path="update_message/(?P<message_pk>[^/.]+)")
    def update_message(self, request, pk=None, message_pk=None):
        message = get_object_or_404(ChatMessage, id=message_pk, user=request.user)

        serializer = ChatMessageSerializerCreate(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["DELETE"],
            serializer_class=ChatMessageSerializerCreate,
            url_path="delete_message/(?P<message_pk>[^/.]+)")
    def delete_message(self, request, pk=None, message_pk=None):
        message = get_object_or_404(ChatMessage, id=message_pk, user=request.user)
        message.delete()

        return Response({"detail": "Message deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
