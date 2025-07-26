# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants
        """
        participant_ids = request.data.get('participants', [])
        
        if not participant_ids:
            return Response(
                {'error': 'Participants are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate that all participant IDs exist
        participants = User.objects.filter(user_id__in=participant_ids)
        if len(participants) != len(participant_ids):
            return Response(
                {'error': 'One or more participants not found'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create conversation and add participants
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['message_body', 'sender__email']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        message_body = request.data.get('message_body')
        
        # Validate required fields
        if not all([conversation_id, sender_id, message_body]):
            return Response(
                {'error': 'conversation_id, sender_id, and message_body are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check if conversation and sender exist
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            sender = User.objects.get(user_id=sender_id)
            
            # Check if sender is part of the conversation
            if sender not in conversation.participants.all():
                return Response(
                    {'error': 'Sender is not part of this conversation'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the message
            message = Message.objects.create(
                sender=sender,
                conversation=conversation,
                message_body=message_body
            )
            
            serializer = self.get_serializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Sender not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def list(self, request, *args, **kwargs):
        """
        List all messages, optionally filtered by conversation
        """
        conversation_id = request.query_params.get('conversation_id', None)
        
        if conversation_id:
            queryset = Message.objects.filter(conversation__conversation_id=conversation_id)
        else:
            queryset = Message.objects.all()
            
        queryset = queryset.order_by('-sent_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)