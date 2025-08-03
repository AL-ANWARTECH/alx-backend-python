# messaging/managers.py
from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a user.
    Usage: Message.unread.unread_for_user(user)
    """
    def unread_for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).only('id', 'sender', 'content', 'timestamp')  # ✅ Optimized with .only()