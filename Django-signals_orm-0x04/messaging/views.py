# messaging/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, UnreadMessageSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import get_object_or_404
from .models import Message

from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return messages involving the current user as sender or receiver.
        Use select_related for efficiency.
        """
        user = self.request.user
        return (
            Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)
        ).select_related('sender', 'receiver', 'parent_message') \
         .prefetch_related('replies') \
         .order_by('sent_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        receiver_id = request.data.get("receiver")
        if not receiver_id:
            return Response({"detail": "Receiver ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({"detail": "Receiver does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, receiver=receiver)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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


# messaging/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Explicitly apply `.only()` in views.py
        unread_messages = Message.unread.unread_for_user(request.user).only(
            'message_id', 'message_body', 'sent_at', 'sender__username'
        )
        serializer = UnreadMessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
