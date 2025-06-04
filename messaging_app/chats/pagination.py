#custom pagination class
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that extends PageNumberPagination.
    This can be used to customize pagination behavior if needed.
    """
    page_size = 20  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set page size via query param
    max_page_size = 100  # Maximum allowed page size

    def get_paginated_response(self, data):
        """
        Override to include additional metadata in the paginated response.
        """
        return super().get_paginated_response(data)
    
    def paginate_queryset(self, queryset, request, view=None):
        """
        Override to handle pagination logic.
        This can be customized further if needed.
        """
        self.request = request
        self.view = view
        self.queryset = queryset

        # Call the parent method to perform pagination
        return super().paginate_queryset(queryset, request, view)
    
    def get_page_size(self, request):
        """
        Override to allow clients to specify page size via query param.
        If not specified, use the default page size.
        """
        if request.query_params.get('page_size'):
            try:
                return min(int(request.query_params['page_size']), self.max_page_size)
            except ValueError:
                return self.page_size
            
        return self.page_size
    
    

