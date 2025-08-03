# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    sender = models.ForeignKey(
        User,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    edited = models.BooleanField(default=False)

    # Self-referential FK: allows replies to messages
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    def __str__(self):
        if self.parent_message:
            return f"Reply by {self.sender} to {self.receiver}"
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']

    def get_all_replies(self):
        """
        Recursively get all replies to this message, including:
        - Direct replies
        - Replies to those replies (nested)
        - And so on...
        Returns a flat list of Message objects.
        """
        all_replies = []
        for reply in self.replies.all():
            all_replies.append(reply)
            # Recursively get deeper replies
            all_replies.extend(reply.get_all_replies())
        return all_replies


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history'
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(default=timezone.now)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Edit history for message {self.message.id}"


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Notification for {self.user.username}"