# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Message, Notification
from .signals import create_notification_on_new_message

class MessagingSignalsTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='test123')
        self.receiver = User.objects.create_user(username='bob', password='test123')

    def test_notification_created_on_new_message(self):
        """A notification should be created when a message is sent."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hi Bob!"
        )
        self.assertTrue(Notification.objects.filter(message=message).exists())
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)

    def test_no_extra_notification_on_update(self):
        """Updating a message should not create another notification."""
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="First message"
        )
        initial_count = Notification.objects.count()
        # Update the message
        message = Message.objects.get()
        message.content = "Updated"
        message.save()
        self.assertEqual(Notification.objects.count(), initial_count)

    def test_signal_disconnection(self):
        """Test can safely disconnect signal."""
        post_save.disconnect(create_notification_on_new_message, sender=Message)
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="No notification"
        )
        self.assertEqual(Notification.objects.count(), 0)
        # Reconnect (for other tests)
        post_save.connect(create_notification_on_new_message, sender=Message)