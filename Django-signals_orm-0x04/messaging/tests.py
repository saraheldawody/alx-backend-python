# messaging/tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()

class NotificationSignalTest(TestCase):
    def setUp(self):
        # Create two users: alice sends to bob
        self.alice = User.objects.create_user(
            username='alice',
            email='alice@example.com',
            password='testpass123'
        )
        self.bob = User.objects.create_user(
            username='bob',
            email='bob@example.com',
            password='testpass123'
        )

    def test_notification_created_on_message(self):
        # Initially, no notifications
        self.assertEqual(Notification.objects.count(), 0)

        # Alice sends a message to Bob
        msg = Message.objects.create(
            sender=self.alice,
            receiver=self.bob,
            content="Hello Bob!"
        )

        # After creating the message, notification should exist
        notifications = Notification.objects.filter(user=self.bob, message=msg)
        self.assertEqual(notifications.count(), 1)

        notification = notifications.first()
        self.assertFalse(notification.is_read)
        # created_at should be close to now; just check it exists
        self.assertIsNotNone(notification.created_at)

    def test_no_notification_for_sender(self):
        # Even if sender and receiver are same (edge case), notification is created for that user.
        # Depending on business logic, you might skip creating if sender == receiver.
        # Here we test that notification is created; adjust if you want to skip.
        user = User.objects.create_user(
            username='charlie',
            email='charlie@example.com',
            password='testpass123'
        )
        msg = Message.objects.create(
            sender=user,
            receiver=user,
            content="Self-message"
        )
        notifications = Notification.objects.filter(user=user, message=msg)
        self.assertEqual(notifications.count(), 1)
