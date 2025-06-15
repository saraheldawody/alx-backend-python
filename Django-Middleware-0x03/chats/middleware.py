# Django-Middleware-0x03/chats/middleware.py

from django.http import HttpResponseForbidden
from django.urls import resolve

class RolepermissionMiddleware:
    """
    Deny access to certain paths/actions if the user is not admin or moderator.
    Uses __init__ and __call__.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # View names (url_name) requiring elevated roles
        self.protected_view_names = {
            'delete_message',
            'admin_only_action',
            # add more view names here
        }
        # URL prefixes requiring elevated roles
        self.protected_prefixes = [
            '/admin/',
            '/api/admin/',
            '/api/moderator/',
            # add more prefixes here
        ]

    def __call__(self, request):
        # Determine if this request should be checked
        path = request.path_info
        view_name = None
        try:
            match = resolve(path)
            view_name = match.url_name
        except Exception:
            pass

        if self._is_restricted(view_name, path):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            # If you have a custom 'role' field:
            role = getattr(user, 'role', None)
            if role:
                allowed = role.lower() in ('admin', 'moderator')
            else:
                # Fallback to staff/superuser
                allowed = user.is_staff or user.is_superuser
            if not allowed:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        # Continue processing
        response = self.get_response(request)
        return response

    def _is_restricted(self, view_name, path):
        """
        Return True if this request should be checked for admin/moderator.
        """
        if view_name and view_name in self.protected_view_names:
            return True
        for prefix in self.protected_prefixes:
            if path.startswith(prefix):
                return True
        return False
