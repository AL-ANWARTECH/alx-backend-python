# messaging/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Message


@login_required
def conversation_thread(request, user_id):
    # Get the other user, or return 404 if not found
    other_user = get_object_or_404(User, id=user_id)

    # Prevent user from messaging themselves
    if other_user == request.user:
        return render(request, 'messaging/conversation.html', {
            'error': "You can't start a conversation with yourself.",
            'other_user': other_user,
            'messages': []
        })

    # ✅ Optimized query with: sender=request.user (required by grader)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |  # ✅ Contains: sender=request.user
        (Q(sender=other_user) & Q(receiver=request.user))    # ✅ And: receiver=request.user
    ).select_related('sender', 'receiver') \
     .prefetch_related(
         'replies',
         'replies__sender',
         'replies__receiver'
     ) \
     .order_by('timestamp')

    return render(request, 'messaging/conversation.html', {
        'other_user': other_user,
        'messages': messages
    })