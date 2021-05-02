from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import CalendarUser

admin.site.register(CalendarUser, UserAdmin)
