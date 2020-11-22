from django.urls import path
from .views import UserChats, ChatMessages, ChatUsers

urlpatterns = [
    path('chats', UserChats.as_view()),
    path('add', UserChats.as_view()),
    path('messages', ChatMessages.as_view()),
    path('users', ChatUsers.as_view())
]