# messaging/admin.py

from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'sent_at')
    list_filter = ('sent_at', 'sender', 'receiver')
    search_fields = ('content', 'sender__username', 'receiver__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_id', 'user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'user')
    search_fields = ('user__username', 'message__content')
