# messaging/serializers.py

from rest_framework import serializers
from .models import Notification
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'receiver', 'content', 'sent_at', 'parent_message']
        read_only_fields = ['message_id', 'sent_at']
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_id', 'message', 'is_read', 'created_at']
        read_only_fields = ['notification_id', 'message', 'created_at']
