# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation, IsOwnerOrParticipant
from .pagination import MessagePagination
from .filters import MessageFilter, ConversationFilter


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = ConversationFilter
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsParticipantOfConversation]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Users can only see conversations they're part of
        if self.request.user.is_authenticated:
            return Conversation.objects.filter(participants=self.request.user)
        return Conversation.objects.none()

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
        
        # Always include the current user as a participant
        if str(request.user.user_id) not in participant_ids:
            participant_ids.append(str(request.user.user_id))
        
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
        Get all messages for a specific conversation with pagination
        """
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('sent_at')
        
        # Apply pagination
        paginator = MessagePagination()
        paginated_messages = paginator.paginate_queryset(messages, request)
        serializer = MessageSerializer(paginated_messages, many=True)
        
        return paginator.get_paginated_response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwnerOrParticipant]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    search_fields = ['message_body', 'sender__email']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        # Users can only see messages from conversations they're part of
        if self.request.user.is_authenticated:
            return Message.objects.filter(
                conversation__participants=self.request.user
            ).distinct()
        return Message.objects.none()

    def perform_create(self, serializer):
        # Automatically set the sender to the current user
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Send a new message to an existing conversation
        """
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')
        
        # Validate required fields
        if not all([conversation_id, message_body]):
            return Response(
                {'error': 'conversation_id and message_body are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Check if conversation exists
            conversation = Conversation.objects.get(conversation_id=conversation_id)
            
            # Check if current user is part of the conversation
            if request.user not in conversation.participants.all():
                return Response(
                    {'error': 'You are not part of this conversation'}, 
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Create the message with current user as sender
            message = Message.objects.create(
                sender=request.user,
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
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def list(self, request, *args, **kwargs):
        """
        List all messages with pagination and filtering
        """
        return super().list(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Update a message (only sender can update)
        """
        instance = self.get_object()
        if instance.sender != request.user:
            return Response(
                {'error': 'You do not have permission to update this message'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a message (only sender can delete)
        """
        instance = self.get_object()
        if instance.sender != request.user:
            return Response(
                {'error': 'You do not have permission to delete this message'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)