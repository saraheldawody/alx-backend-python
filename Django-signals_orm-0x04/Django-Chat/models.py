# Django-Chat/Models.py

import uuid
from django.conf import settings
from django.db import models

class Message(models.Model):
    """
    Represents a message sent in a chat. 
    Now includes tracking for edits.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # Track if message has been edited

    def __str__(self):
        return f"Message {self.message_id} from {self.sender} to {self.receiver}"

class MessageHistory(models.Model):
    """
    Stores old versions of a message before edits.
    """
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history of Message {self.message.message_id} at {self.edited_at}"
