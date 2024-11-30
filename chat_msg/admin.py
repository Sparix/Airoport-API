from django.contrib import admin

from chat_msg.models import ChatMessage, ChatSupport


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user",)

@admin.register(ChatSupport)
class ChatSupportAdmin(admin.ModelAdmin):
    list_display = ("chat_support_group",)
