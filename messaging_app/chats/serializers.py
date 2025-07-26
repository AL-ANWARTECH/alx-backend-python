# chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    display_role = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'full_name', 'display_role', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()
    formatted_sent_at = serializers.CharField(source='sent_at', read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'message_preview', 'formatted_sent_at', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def get_message_preview(self, obj):
        return obj.message_body[:50] + "..." if len(obj.message_body) > 50 else obj.message_body


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    latest_message = serializers.SerializerMethodField()
    conversation_status = serializers.CharField(default="active", read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_count', 'conversation_status', 'messages', 'latest_message', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_participant_count(self, obj):
        return obj.participants.count()
    
    def get_latest_message(self, obj):
        latest_msg = obj.messages.order_by('-sent_at').first()
        if latest_msg:
            return MessageSerializer(latest_msg).data
        return None
    
    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value