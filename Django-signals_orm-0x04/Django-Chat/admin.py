# Django-Chat/admin.py

from django.contrib import admin
from .models import Message, MessageHistory

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'receiver', 'sent_at', 'edited')

@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('history_id', 'message', 'edited_at')
