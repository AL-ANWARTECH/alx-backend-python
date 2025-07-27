# chats/filters.py

import django_filters
from django.db import models
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    """
    Filter class for messages
    """
    # Filter by sender
    sender_id = django_filters.UUIDFilter(field_name='sender__user_id')
    sender_email = django_filters.CharFilter(field_name='sender__email', lookup_expr='icontains')
    
    # Filter by conversation participants
    participant_id = django_filters.UUIDFilter(method='filter_by_participant')
    participant_email = django_filters.CharFilter(method='filter_by_participant_email')
    
    # Filter by date range
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    
    # Filter by conversation
    conversation_id = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    
    # Filter by message content
    message_content = django_filters.CharFilter(field_name='message_body', lookup_expr='icontains')

    class Meta:
        model = Message
        fields = [
            'sender_id',
            'sender_email',
            'conversation_id',
            'message_content',
        ]

    def filter_by_participant(self, queryset, name, value):
        """Filter messages by conversation participants"""
        return queryset.filter(conversation__participants__user_id=value)

    def filter_by_participant_email(self, queryset, name, value):
        """Filter messages by conversation participant email"""
        return queryset.filter(conversation__participants__email__icontains=value)


class ConversationFilter(django_filters.FilterSet):
    """
    Filter class for conversations
    """
    # Filter by participants
    participant_id = django_filters.UUIDFilter(field_name='participants__user_id')
    participant_email = django_filters.CharFilter(field_name='participants__email', lookup_expr='icontains')
    
    # Filter by date range
    start_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Conversation
        fields = [
            'participant_id',
            'participant_email',
        ]