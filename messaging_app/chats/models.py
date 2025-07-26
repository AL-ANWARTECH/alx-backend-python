from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

# Create your models here.
class User(AbstractUser):
    # Add custom fields
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]

class Conversation(models.Model):
    Conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversation')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.Conversation_id}"
    
    class Meta:
        db_table = 'conversation'

class Message(models.Model):
    Message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} in {self.conversation.Conversation_id}"
    
    class Meta:
        db_table = 'message'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['sent_at']),
        ]