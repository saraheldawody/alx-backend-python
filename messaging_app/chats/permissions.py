# messaging_app/chats/permissions.py

from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users may access (checked by IsAuthenticated in settings.py).
    - Only participants of a conversation can view, send, update, or delete messages in that conversation.
    - Only participants of a conversation can view or modify the Conversation itself.
    """

    def has_object_permission(self, request, view, obj):
        """
        obj may be either a Conversation or a Message instance:
        - If obj is a Conversation, ensure request.user is in obj.participants.
        - If obj is a Message, ensure request.user is in obj.conversation.participants.
        For unsafe methods on Message (PUT/PATCH/DELETE), we also ensure that only the original sender may modify/delete that message.
        """
        if not request.user.is_authenticated:
            return False
        # If the view is acting on a Conversation instance
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If the view is acting on a Message instance
        if isinstance(obj, Message):
            # Allow only participants of the parent conversation to even see/read this message:
            if request.method in permissions.SAFE_METHODS:
                return request.user in obj.conversation.participants.all()

            # For write operations on a Message (PUT, PATCH, DELETE):
            # Only the original sender may modify/delete their own message.
            return (request.user in obj.conversation.participants.all()
                    and obj.sender == request.user)

        # In all other cases, deny
        return False
