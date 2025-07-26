# messaging_app/chats/urls.py

from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

# This is NestedDefaultRouter - you DON'T want this for the current checker
nested_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
# nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = router.urls + nested_router.urls