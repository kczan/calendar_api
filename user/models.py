import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CalendarUser(AbstractUser):
    company_id = models.UUIDField(default=uuid.uuid4)