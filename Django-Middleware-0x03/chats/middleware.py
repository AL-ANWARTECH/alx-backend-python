import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden


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
