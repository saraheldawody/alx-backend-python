# messaging/signals.py

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model
User = get_user_model()

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


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete sent and received messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete message history related to the user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()

    # Delete user notifications (if applicable)
    Notification.objects.filter(user=instance).delete()

