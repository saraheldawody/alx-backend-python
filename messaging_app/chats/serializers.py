# messaging_app/chats/serializers.py

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    """
    class Meta:
        model = User
        fields = ('user_id', 'username', 'email', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model. 
    Includes nested sender information.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            'message_id',
            'conversation',
            'sender',
            'message_body',
            'sent_at',
        )
        read_only_fields = ('message_id', 'sent_at')


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    Includes nested participants and nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        )
        read_only_fields = ('conversation_id', 'created_at')
