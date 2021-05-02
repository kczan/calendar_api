from django.db import models

from user.models import CalendarUser

class ConferenceRoom(models.Model):
    manager = models.ForeignKey(CalendarUser, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=30)
    address = models.CharField(blank=False, max_length=60)
