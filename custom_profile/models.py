from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    domain = models.CharField(max_length=255, default='example.com')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.username
