from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination.
    This includes explicit reference to page.paginator.count.
    """
    page_size = 20  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set page size via query param
    max_page_size = 100  # Maximum allowed page size

    def paginate_queryset(self, queryset, request, view=None):
        """
        Override to handle pagination logic.
        """
        self.request = request
        self.view = view
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view)
    
    def get_page_size(self, request):
        """
        Allow clients to specify page size via query param.
        """
        if request.query_params.get('page_size'):
            try:
                return min(int(request.query_params['page_size']), self.max_page_size)
            except ValueError:
                return self.page_size
        return self.page_size

    def get_paginated_response(self, data):
        """
        Override to include explicit count via page.paginator.count.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
