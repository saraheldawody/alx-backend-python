import time
from collections import deque, defaultdict
from django.http import HttpResponseTooManyRequests  # Django ≥4.2
# For older Django, use:
# from django.http import HttpResponse
# HttpResponseTooManyRequests = lambda *args, **kwargs: HttpResponse(status=429)

class OffensiveLanguageMiddleware:
    """
    Rejects further POST chat messages from an IP if they exceed
    5 messages within the last 60 seconds.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # map IP -> deque of recent request timestamps
        self.ip_timestamps = defaultdict(deque)
        self.rate_limit = 5        # max messages
        self.window_seconds = 60   # per 60-second window

    def __call__(self, request):
        # Only apply to POST chat-message endpoints; adjust your path as needed
        if request.method == 'POST' and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = time.time()
            timestamps = self.ip_timestamps[ip]

            # Pop timestamps older than window
            while timestamps and now - timestamps[0] > self.window_seconds:
                timestamps.popleft()

            if len(timestamps) >= self.rate_limit:
                return HttpResponseTooManyRequests(
                    "Rate limit exceeded: max 5 messages per minute."
                )

            # Record current request
            timestamps.append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        """
        Retrieves client IP address accounting for proxies if needed.
        """
        xff = request.META.get('HTTP_X_FORWARDED_FOR')
        if xff:
            # in case of multiple IPs, take the left-most
            return xff.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
