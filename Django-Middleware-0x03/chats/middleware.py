# chats/middleware.py

import logging
from datetime import datetime
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