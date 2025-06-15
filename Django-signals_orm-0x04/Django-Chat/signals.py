# Django-Chat/signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message; nothing to track yet

    try:
        previous = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return  # No existing message; nothing to track

    if previous.content != instance.content:
        # Log the old content
        MessageHistory.objects.create(
            message=instance,
            old_content=previous.content
        )
        instance.edited = True
