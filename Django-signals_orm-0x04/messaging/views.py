# messaging/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User  # ✅ Added: Required to use User
from .models import Message


@login_required
def conversation_thread(request, user_id):
    # Get the other user, or return 404 if not found
    other_user = get_object_or_404(User, id=user_id)
    current_user = request.user

    # Prevent user from messaging themselves (optional)
    if other_user == current_user:
        return render(request, 'messaging/conversation.html', {
            'error': "You can't start a conversation with yourself.",
            'other_user': other_user,
            'messages': []
        })

    # ✅ Optimized query: Fetch messages with sender/receiver and all replies
    messages = Message.objects.filter(
        (Q(sender=current_user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=current_user))
    ).select_related('sender', 'receiver') \
     .prefetch_related(
         'replies',           # All direct replies
         'replies__sender',   # Sender of each reply
         'replies__receiver'  # Receiver of each reply
     ) \
     .order_by('timestamp')

    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages
    })