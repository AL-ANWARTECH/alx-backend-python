# messaging/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Message, Notification
from .signals import create_notification_on_new_message  # Important!

class MessagingSignalsTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='test123')
        self.receiver = User.objects.create_user(username='bob', password='test123')

    def test_notification_created_on_new_message(self):
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )
        self.assertTrue(Notification.objects.filter(message__content="Hello!").exists())

    def test_no_duplicate_on_update(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hi")
        initial_count = Notification.objects.count()
        msg.content = "Updated"
        msg.save()
        self.assertEqual(Notification.objects.count(), initial_count)

    def test_signal_disconnection(self):
        post_save.disconnect(create_notification_on_new_message, sender=Message)
        Message.objects.create(sender=self.sender, receiver=self.receiver, content="Silent")
        self.assertEqual(Notification.objects.count(), 0)
        post_save.connect(create_notification_on_new_message, sender=Message)