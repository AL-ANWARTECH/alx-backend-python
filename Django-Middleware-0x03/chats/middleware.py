import logging
from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden
from django.core.cache import cache


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

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        # Process request
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to messaging services outside 6 PM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()

        # Allowed window: 6 PM - 9 PM
        start_time, end_time = time(18, 0), time(21, 0)

        # Restrict access if outside allowed time
        if not (start_time <= current_time <= end_time):
            if not request.path.startswith('/admin/'):
                if any(request.path.startswith(api) for api in [
                    '/api/conversations/', '/api/messages/', '/api/token/'
                ]):
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
        # Time window in seconds (1 minute)
        self.time_window = 60
        # Maximum messages allowed per time window
        self.max_messages = 5

    def __call__(self, request):
        # Only apply to POST requests to message endpoints
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            # Get the client's IP address
            ip_address = self.get_client_ip(request)
            
            # Create a unique cache key for this IP
            cache_key = f"message_count_{ip_address}"
            
            # Get current count and timestamp from cache
            data = cache.get(cache_key)
            
            if data is None:
                # First message from this IP in the time window
                data = {'count': 1, 'first_request': datetime.now()}
                cache.set(cache_key, data, self.time_window)
            else:
                # Check if the time window has expired
                time_passed = datetime.now() - data['first_request']
                if time_passed.total_seconds() > self.time_window:
                    # Reset the count as the window has expired
                    data = {'count': 1, 'first_request': datetime.now()}
                    cache.set(cache_key, data, self.time_window)
                else:
                    # Increment the count
                    data['count'] += 1
                    # Update cache (extend expiration)
                    cache.set(cache_key, data, self.time_window)
                    
                    # Check if limit is exceeded
                    if data['count'] > self.max_messages:
                        return HttpResponseForbidden(
                            f"Rate limit exceeded. You can only send {self.max_messages} messages per minute."
                        )
        
        # Process the request normally
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip