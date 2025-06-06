# messaging_app/chats/views.py

from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from chats.permissions import  IsParticipantOfConversation
from chats.filters import MessageFilter

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    - Supports filtering (e.g. search, ordering) via DRF filters.
    """
    
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['conversation_id']

    def get_queryset(self):
        """
        Restrict to conversations the current user participates in.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)

    @action(detail=True, methods=['post'], url_path='add-participant')
    def add_participant(self, request, pk=None):
        """
        Custom action to add a participant to an existing conversation.
        Expects payload: { "user_id": "<uuid-of-user-to-add>" }
        """
        conv = get_object_or_404(self.get_queryset(), conversation_id=pk)
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {"detail": "user_id is required to add a participant."},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user_to_add = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": f"User with id {user_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        conv.participants.add(user_to_add)
        conv.save()
        return Response(
            {"detail": f"User {user_id} added to conversation {pk}."},
            status=status.HTTP_200_OK
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating messages.
    - Supports filtering by conversation via query params.
    """
    queryset = Message.objects.all().order_by('sent_at')
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    search_fields = ['message_body']

    def get_queryset(self):
        """
        Optionally filter messages by conversation_id query parameter.
        e.g. GET /messages/?conversation=<conversation_id>
        """
        qs = super().get_queryset()
        conv_id = self.request.query_params.get('conversation')
        if conv_id:
            qs = qs.filter(conversation__conversation_id=conv_id)
        return qs

    def perform_create(self, serializer):
        """
        When creating a new message, automatically set sender to the current user.
        """
        serializer.save(sender=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Validate conversation exists and user is a participant before allowing creation.
        Expects:
        {
            "conversation": "<conversation_uuid>",
            "message_body": "Hello, world!"
        }
        """
        conversation_id = request.data.get('conversation')
        if not conversation_id:
            return Response(
                {"detail": "conversation (UUID) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": f"Conversation with id {conversation_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)
