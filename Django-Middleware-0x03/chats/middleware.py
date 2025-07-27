import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.utils import timezone  # Use timezone-aware datetime


class RequestLoggingMiddleware:
    """
    Middleware to log user requests including timestamp, user, and request path.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

    def __call__(self, request):
        # Determine user identity
        user = request.user.email if request.user.is_authenticated else 'AnonymousUser'

        # Log the request with timezone-aware timestamp
        log_message = f"{timezone.localtime()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to messaging services outside 6 PM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = timezone.localtime().time()

        # Allowed window: 6 PM - 9 PM
        start_time, end_time = time(18, 0), time(21, 0)

        # Restrict access if outside allowed time (but allow admin panel)
        if not (start_time <= current_time <= end_time):
            if not request.path.startswith('/admin/'):
                protected_paths = ['/api/conversations/', '/api/messages/', '/api/token/']
                if any(request.path.startswith(api) for api in protected_paths):
                    return HttpResponseForbidden(
                        "Access to messaging services is restricted. "
                        "Available between 6:00 PM and 9:00 PM only."
                    )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages a user (IP) can send per minute.
    Limits to 5 messages per minute per IP.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = 60  # seconds
        self.max_messages = 5

    def __call__(self, request):
        # Only apply to POST requests to message endpoints
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip_address = self.get_client_ip(request)
            cache_key = f"message_count_{ip_address}"
            data = cache.get(cache_key)

            now = timezone.now()  # Use timezone-aware time

            if data is None:
                data = {'count': 1, 'first_request': now}
                cache.set(cache_key, data, self.time_window)
            else:
                time_passed = (now - data['first_request']).total_seconds()
                if time_passed > self.time_window:
                    data = {'count': 1, 'first_request': now}
                else:
                    data['count'] += 1
                    if data['count'] > self.max_messages:
                        return HttpResponseForbidden(
                            f"Rate limit exceeded. You can only send {self.max_messages} messages per minute."
                        )
                cache.set(cache_key, data, self.time_window)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class RolepermissionMiddleware:
    """
    Middleware that checks the user's role (admin or moderator) before allowing access to specific actions.
    If the user is not admin or moderator, it returns a 403 Forbidden error.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that require admin or moderator role
        # Example: Admin panel, user management, etc.
        # You can adjust these paths based on your specific requirements
        protected_admin_paths = [
            '/admin/',
            # Add other paths that should be restricted to admins/moderators
        ]
        
        # Check if the request path is in the protected paths
        if any(request.path.startswith(path) for path in protected_admin_paths):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Access denied. You must be logged in.")
            
            # Check user role
            # Assuming your custom User model has a 'role' field with values like 'admin', 'moderator', 'guest', 'host'
            user_role = getattr(request.user, 'role', None)
            
            # Allow access if user is admin or moderator
            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden(
                    "Access denied. You must be an admin or moderator to access this resource."
                )

        # Process the request normally for all other cases
        return self.get_response(request)