from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    completed_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=0)