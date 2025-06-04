# messaging_app/chats/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


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
    Explicitly declare message_body as CharField and validate non-empty content.
    """
    message_body = serializers.CharField()
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

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model.
    - Accepts a list of participant user_ids on write (write-only CharField list).
    - Returns nested participant info and nested messages on read.
    """
    # Accept a list of UUID strings representing user_ids
    participants = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )
    # Return nested participant details
    participants_info = serializers.SerializerMethodField()
    # Return nested messages
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participants',
            'participants_info',
            'created_at',
            'messages',
        )
        read_only_fields = ('conversation_id', 'created_at', 'participants_info', 'messages')

    def get_participants_info(self, obj):
        """
        Return serialized User objects for all participants.
        """
        users = obj.participants.all()
        return UserSerializer(users, many=True).data

    def validate_participants(self, value):
        """
        Ensure at least two distinct participants are provided.
        """
        if len(value) < 2:
            raise serializers.ValidationError("A conversation requires at least two participants.")
        if len(set(value)) != len(value):
            raise serializers.ValidationError("Participant list contains duplicates.")
        # Ensure all provided IDs correspond to existing users
        missing = []
        for uid in value:
            try:
                User.objects.get(user_id=uid)
            except User.DoesNotExist:
                missing.append(uid)
        if missing:
            raise serializers.ValidationError(f"User(s) with ID(s) {missing} do not exist.")
        return value

    def create(self, validated_data):
        """
        Create Conversation and attach participants.
        """
        participant_ids = validated_data.pop('participants', [])
        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        return conversation

    def to_representation(self, instance):
        """
        Use default representation but omit the writable 'participants' field.
        """
        rep = super().to_representation(instance)
        rep.pop('participants', None)
        return rep
