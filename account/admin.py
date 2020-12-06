from django.contrib import admin
from .models import Profile, UserSettings, UserFollowing


admin.site.register(Profile)
admin.site.register(UserSettings)
admin.site.register(UserFollowing)

