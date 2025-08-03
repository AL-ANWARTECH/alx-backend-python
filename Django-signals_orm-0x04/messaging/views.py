# messaging/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


@login_required
def delete_user(request):
    """
    Allow the logged-in user to delete their account.
    On POST, delete the user and log them out.
    """
    if request.method == 'POST':
        user = request.user
        username = user.username

        # Django's User model delete will trigger post_delete signal
        user.delete()

        # Log out and show message
        logout(request)
        messages.success(request, f"Account '{username}' has been deleted permanently.")
        return redirect('delete_user')  # Redirect to a success page (same view)

    return render(request, 'messaging/delete_user.html')