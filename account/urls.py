from django.urls import path
from .views import (UserRegistration, UserLogin, 
UserFollowings, UserProfile, follow_action, UpdateUserSettings, UserSettingsDetails)
from rest_framework.authtoken import views

urlpatterns = [
    path('new', UserRegistration.as_view()),
    path('login', UserLogin.as_view()),
    path('following', UserFollowings.as_view()),
    path('profile', UserProfile.as_view()),
    path('profile/edit', UserProfile.as_view()),
    path('profile/follow_unfollow', follow_action),
    path('settings', UpdateUserSettings.as_view()),
    path('settings/details', UserSettingsDetails.as_view())
]