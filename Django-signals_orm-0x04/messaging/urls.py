# messaging/urls.py
from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('delete/', views.delete_user, name='delete_user'),
]