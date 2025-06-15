import os
from datetime import datetime
from django.conf import settings

class RequestLoggingMiddleware:
    """
    Logs each request’s timestamp, user, and path to a file.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Determine log file path; adjust filename or location if desired
        # BASE_DIR is typically defined in settings.py as project root
        base_dir = getattr(settings, 'BASE_DIR', None)
        if base_dir:
            self.log_file_path = os.path.join(base_dir, 'request_logs.log')
        else:
            # fallback: current directory
            self.log_file_path = 'request_logs.log'

    def __call__(self, request):
        # Get user identifier; handle anonymous
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        # Format timestamp; you can choose timezone-aware if needed
        timestamp = datetime.now().isoformat()
        line = f"{timestamp} - User: {user} - Path: {request.path}\n"
        try:
            with open(self.log_file_path, 'a') as f:
                f.write(line)
        except Exception:
            # Silently ignore logging failures to avoid breaking requests
            pass

        response = self.get_response(request)
        return response
