# messaging/apps.py

from django.apps import AppConfig

class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        # Import signals to ensure they are registered
        from . import signals  # noqa
