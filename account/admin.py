from django.contrib import admin
from .models import Profile, UserSettings


admin.site.register(Profile)
admin.site.register(UserSettings)

