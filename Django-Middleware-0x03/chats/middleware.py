# chats/middleware.py

import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class RequestLoggingMiddleware:
    """
    Middleware to log user requests including timestamp, user, and request path
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up logger
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler if it doesn't exist
        if not self.logger.handlers:
            handler = logging.FileHandler('requests.log')
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.propagate = False

    def __call__(self, request):
        # Get user information
        user = getattr(request.user, 'email', 'AnonymousUser')
        if user == 'AnonymousUser' and hasattr(request.user, 'is_anonymous') and request.user.is_anonymous:
            user = 'AnonymousUser'
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app during certain hours.
    Denies access outside 6 PM and 9 PM.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time
        current_time = datetime.now().time()
        
        # Define restricted time range: outside 6 PM to 9 PM
        start_time = time(18, 0)   # 6:00 PM
        end_time = time(21, 0)     # 9:00 PM
        
        # Check if current time is outside allowed range (i.e., within restricted hours)
        if current_time < start_time or current_time > end_time:
            # Allow access to admin pages even outside hours
            if not request.path.startswith('/admin/'):
                # Check if the request is for messaging API endpoints
                if (request.path.startswith('/api/conversations/') or 
                    request.path.startswith('/api/messages/') or 
                    request.path.startswith('/api/token/')):
                    return HttpResponseForbidden(
                        "Access to messaging services is restricted. "
                        "Available between 6:00 PM and 9:00 PM only."
                    )
        
        # Process the request normally
        response = self.get_response(request)
        return response