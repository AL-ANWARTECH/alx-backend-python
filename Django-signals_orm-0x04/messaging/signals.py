# messaging/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, MessageHistory, Notification


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before saving, check if the message is being updated and content has changed.
    If yes, save the old content to MessageHistory and mark as edited.
    """
    if instance.pk:  # Only if it's an existing message (update)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_at=timezone.now(),
                    edited_by=instance.sender  # Assuming sender is editing
                )
                instance.edited = True  # Mark message as edited
        except Message.DoesNotExist:
            pass  # Being created for the first time — ignore


@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    From Task 0: Create notification when a new message is sent.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )