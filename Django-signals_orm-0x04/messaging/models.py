# messaging/models.py

import uuid
from django.conf import settings
from django.db import models

class Message(models.Model):
    """
    Represents a message sent from one user to another.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_messages',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender} to {self.receiver}"

class Notification(models.Model):
    """
    Notification created when a user receives a new message.
    """
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # optional: show newest first by default
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification {self.notification_id} for {self.user} about Message {self.message.message_id}"
