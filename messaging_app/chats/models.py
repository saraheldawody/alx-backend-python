# messaging_app/chats/models.py

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's built-in AbstractUser.
    This model includes additional fields for phone number, bio, and avatar.
    """
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    Tracks a conversation involving multiple users.
    The participants field creates a many-to-many link to User.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message sent by a user within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        related_name='messages',
        on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} by {self.sender} in Conversation {self.conversation.id}"
