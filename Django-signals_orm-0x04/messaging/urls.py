from messaging.views import UnreadMessagesView, delete_user
from django.urls import path
urlpatterns = [
    # ...
    path('delete-account/', delete_user, name='delete_user'),
    path('messages/unread/', UnreadMessagesView.as_view(), name='unread-messages'),
]
