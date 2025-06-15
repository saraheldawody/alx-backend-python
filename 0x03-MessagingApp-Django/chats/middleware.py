from datetime import time
from django.utils import timezone
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Deny access to chat-related endpoints outside 18:00–21:00 local server time.
    Adjust `is_chat_path` logic if your chat URLs differ.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Define allowed window
        self.start_time = time(hour=18, minute=0)  # 6PM
        self.end_time = time(hour=21, minute=0)    # 9PM

    def __call__(self, request):
        # Only restrict certain paths; adjust as needed
        path = request.path
        if self.is_chat_path(path):
            # Get current local time (aware)
            now = timezone.localtime(timezone.now())
            current_time = now.time()
            # Allow if within [18:00, 21:00). Deny otherwise.
            if not (self.start_time <= current_time < self.end_time):
                return HttpResponseForbidden("Access to chat is allowed only between 18:00 and 21:00.")
        # Continue normally
        response = self.get_response(request)
        return response

    def is_chat_path(self, path: str) -> bool:
        """
        Determine whether this request should be restricted by time.
        For example, restrict URLs under /api/messages/ or /api/conversations/.
        Adjust patterns to fit your routing.
        """
        # Example checks; modify to match your URL patterns:
        restricted_prefixes = [
            '/api/messages/',
            '/api/conversations/',
            '/chats/',        # if you have chat URLs here
            '/messages/',
            '/conversations/',
        ]
        return any(path.startswith(prefix) for prefix in restricted_prefixes)
