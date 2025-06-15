# messaging/signals.py

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """
    After a Message is created, create a Notification for the receiver.
    """
    if created:
        # Create a notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

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
            old_content=previous.content,
            edited_by=instance.sender  # Assuming the sender is the one editing
        )
        instance.edited = True
