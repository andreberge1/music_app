from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    spotifyuser = models.CharField(max_length=25)

    def __str__(self):
        return self.username
