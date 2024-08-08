from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    completed_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=0)
    country = models.TextField(default="")
    city = models.TextField(default="")
    latitude = models.FloatField(default="0")
    longitude = models.FloatField(default="0")
    timezone = models.IntegerField(default=0)