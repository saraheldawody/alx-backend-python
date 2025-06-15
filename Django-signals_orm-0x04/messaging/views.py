# messaging/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and retrieve notifications for the current user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response({'status': 'marked as read'})


# Django-Chat/views.py

from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_user(request):
    """
    Authenticated user deletes their account.
    This triggers post_delete signal to clean related data.
    """
    user = request.user
    user.delete()
    return Response({'detail': 'Your account and related data have been deleted.'}, status=status.HTTP_204_NO_CONTENT)


