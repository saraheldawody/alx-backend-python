# Django-Middleware-0x03/chats/middleware.py

from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve

class RolepermissionMiddleware(MiddlewareMixin):
    """
    Deny access to certain paths/actions if the user is not admin or moderator.
    Adjust `is_restricted_path` logic to match your URLs or view names.
    """

    def __init__(self, get_response=None):
        super().__init__(get_response)
        # If you have specific view names or URL prefixes to protect, list them here:
        # e.g., protect view names: ['delete_message', 'admin_panel']
        self.protected_view_names = {
            'delete_message',
            'admin_only_action',
            # add more view names that require admin/moderator
        }
        # Or protect URL prefixes:
        self.protected_prefixes = [
            '/admin/', 
            '/api/admin/', 
            '/api/moderator/',
            # add more prefixes as needed
        ]

    def process_request(self, request):
        user = request.user
        # If user is not authenticated, immediately forbid on protected paths
        path = request.path_info  # e.g., "/api/messages/delete/..."
        # Check by view name if you prefer:
        try:
            match = resolve(path)
            view_name = match.url_name
        except Exception:
            view_name = None

        if self.is_restricted(view_name, path):
            # Check if user is allowed: either a custom role field or Django flags
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            # Example: if you have a 'role' attribute on user:
            role = getattr(user, 'role', None)
            if role:
                allowed = role.lower() in ('admin', 'moderator')
            else:
                # fallback to Django staff/superuser
                allowed = user.is_staff or user.is_superuser
            if not allowed:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        # Otherwise allow
        return None  # continue processing

    def is_restricted(self, view_name, path):
        """
        Return True if this request should be checked for admin/moderator.
        Adjust logic: by view_name or by path prefix.
        """
        if view_name and view_name in self.protected_view_names:
            return True
        for prefix in self.protected_prefixes:
            if path.startswith(prefix):
                return True
        return False
