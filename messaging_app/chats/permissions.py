# messaging_app/chats/permissions.py

from rest_framework import permissions
from .models import Conversation, Message


class IsConversationParticipant(permissions.BasePermission):
    """
    Only allow users who are participants in a given conversation
    to retrieve/update/delete it.
    """

    def has_object_permission(self, request, view, obj: Conversation):
        # obj is a Conversation instance
        return request.user in obj.participants.all()


class IsMessageParticipantOrSender(permissions.BasePermission):
    """
    Only allow users who are part of the conversation to view messages,
    and only the sender to update/delete their own message.
    """

    def has_object_permission(self, request, view, obj: Message):
        # obj is a Message instance.
        # If reading (GET/list), ensure the requesting user is in that conversation.
        if request.method in permissions.SAFE_METHODS:
            return request.user in obj.conversation.participants.all()
        # For write (PUT/PATCH/DELETE), only the original sender can modify or delete.
        return obj.sender == request.user
