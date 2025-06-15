# messaging_app/messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include

from chats.auth import MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT auth endpoints:
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

    # Browseable DRF login/logout (optional, but recommended for session‐based testing)
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),

    # All chat‐related API endpoints (conversations & messages):
    path('api/', include('chats.urls')),
]
