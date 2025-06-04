# messaging_app/chats/filters.py

import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    Allows filtering messages by:
      - conversation UUID
      - sender UUID
      - sent_at >= sent_after
      - sent_at <= sent_before
    """
    conversation = django_filters.UUIDFilter(
        field_name='conversation__conversation_id',
        lookup_expr='exact',
        help_text='Filter messages by conversation UUID'
    )
    sender = django_filters.UUIDFilter(
        field_name='sender__user_id',
        lookup_expr='exact',
        help_text='Filter messages by sender UUID'
    )
    sent_after = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        help_text='Filter messages sent at or after this timestamp'
    )
    sent_before = django_filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        help_text='Filter messages sent at or before this timestamp'
    )

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_after', 'sent_before']
