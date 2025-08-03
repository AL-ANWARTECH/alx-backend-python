# messaging/signals.py
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Message, MessageHistory, Notification


# === Task 1: Log edits (pre_save) ===
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_at=timezone.now(),
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


# === Task 0: Notification on new message (post_save) ===
@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


# === Task 2: Cleanup on user delete (post_delete) ===
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    When a User is deleted, remove all related messages, notifications, and history.
    Django CASCADE will handle most, but we do it explicitly for clarity and safety.
    """
    # Delete all messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications for this user
    Notification.objects.filter(user=instance).delete()

    # Delete all message history entries where user was edited_by
    MessageHistory.objects.filter(edited_by=instance).delete()

    # Note: CASCADE on ForeignKey would also delete these if set,
    # but this signal ensures full cleanup even if CASCADE is not used.