from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('delete/', views.delete_user, name='delete_user'),
    path('conversation/<int:user_id>/', views.conversation_thread, name='conversation'),
    path('login/', LoginView.as_view(), name='login'),  # Optional
]