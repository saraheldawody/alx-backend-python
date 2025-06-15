# Django-Chat/apps.py

from django.apps import AppConfig

class DjangoChatConfig(AppConfig):
    name = 'Django-Chat'

    def ready(self):
        from . import signals  # Ensure signals are loaded
