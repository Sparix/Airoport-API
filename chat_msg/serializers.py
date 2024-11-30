from rest_framework import serializers

from chat_msg.models import ChatSupport, ChatMessage
from user.serializers import UserSerializer


class ChatSupportConnectChatSerializer(serializers.ModelSerializer):
    user_list = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSupport
        fields = ("user_list",)


class ChatSupportSerializerBase(ChatSupportConnectChatSerializer):
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )
    author_created = UserSerializer(read_only=True)

    class Meta(ChatSupportConnectChatSerializer.Meta):
        fields = ChatSupportConnectChatSerializer.Meta.fields + (
            "id",
            "chat_support_group",
            "enabled",
            "created_at",
            "author_created",
            "is_support",
        )


class ChatSupportSerializer(ChatSupportSerializerBase):
    author_created = UserSerializer(read_only=True)


class ChatMessageSerializerBase(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = ChatMessage
        fields = ("id", "body_msg", "created_at", "user", "is_read", "support_msg")


class ChatMessageSerializerCreate(ChatMessageSerializerBase):
    support_msg = serializers.PrimaryKeyRelatedField(
        queryset=ChatSupport.objects.all(),
        required=True
    )

class ChatMessageSerializer(ChatMessageSerializerBase):
    support_msg = ChatSupportSerializer(read_only=True)


class ChatSupportSerializerRetrieve(ChatSupportSerializer):
    messages = ChatMessageSerializerBase(many=True, read_only=True, source='chatmessage_set')

    class Meta(ChatSupportSerializer.Meta):
        fields = ChatSupportSerializer.Meta.fields + ("messages",)
