from django.db import models

from django.conf import settings


class ChatSupport(models.Model):
    chat_support_group = models.CharField(max_length=100, unique=True)
    enabled = models.BooleanField(default=True)
    author_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_chats',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_support = models.BooleanField(default=False)
    user_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name = 'participated_chats',
    )

    def __str__(self):
        return self.chat_support_group

class ChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    support_msg = models.ForeignKey(
        'ChatSupport', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    body_msg = models.TextField()

    def __str__(self):
        return f"{self.user}: {self.support_msg.chat_support_group}"