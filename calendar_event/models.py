from django.db import models

from room.models import ConferenceRoom
from user.models import CalendarUser


class Event(models.Model):
    owner = models.ForeignKey(
        verbose_name="event_owner",
        to=CalendarUser,
        on_delete=models.CASCADE,
        related_name="event_owner",
    )
    name = models.CharField(verbose_name="event_name", blank=False, max_length=30)
    agenda = models.CharField(verbose_name="event_agenda", blank=False, max_length=40)
    start = models.DateTimeField(verbose_name="event_start_date", blank=False)
    end = models.DateTimeField(verbose_name="event_end_date", blank=False)
    participants = models.ManyToManyField(
        verbose_name="event_participants",
        to=CalendarUser,
        blank=True,
        related_name="event_participants",
    )
    location = models.ForeignKey(
        verbose_name="event_location",
        to=ConferenceRoom,
        blank=True,
        on_delete=models.CASCADE,
    )
