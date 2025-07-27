# chats/permissions.py

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to:
    - Send messages to the conversation
    - View messages in the conversation
    - Update/delete their own messages
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read access to participants only
        if request.method in permissions.SAFE_METHODS:
            # For Conversation objects
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            # For Message objects
            elif hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
        
        # Write permissions - only for participants
        if hasattr(obj, 'participants'):
            # Conversation object
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # Message object
            return request.user in obj.conversation.participants.all()
        
        return False
    
    def has_permission(self, request, view):
        # Allow authenticated users to access the API
        return request.user and request.user.is_authenticated


class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow:
    - Owners to edit/delete their own messages
    - Participants to view messages in conversations they're part of
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow read access to participants
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            elif hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
        
        # Write permissions - only for message owners
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        elif hasattr(obj, 'user_id'):
            return obj.user_id == request.user.user_id
            
        return False
    
    def has_permission(self, request, view):
        # Allow authenticated users to access the API
        return request.user and request.user.is_authenticated


class IsAuthenticatedAndOwner(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to access their own data
    """
    
    def has_object_permission(self, request, view, obj):
        # Read and write permissions are only allowed to the owner of the object
        if hasattr(obj, 'sender'):
            return obj.sender == request.user
        elif hasattr(obj, 'user_id'):
            return obj.user_id == request.user.user_id
        return False
    
    def has_permission(self, request, view):
        # Allow authenticated users to access the API
        return request.user and request.user.is_authenticated