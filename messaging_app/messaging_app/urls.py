# messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # All chat-related API routes live under /api/
    path('api/', include('messaging_app.chats.urls')),
]
