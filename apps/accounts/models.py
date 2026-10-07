from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import UUIDTimeStampedModel


class User(UUIDTimeStampedModel, AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    recovery_phrase_hash = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
