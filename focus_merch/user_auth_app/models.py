from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=1000, null=True)
    bio = models.CharField(max_length=1000, null=True)

    USERNAME_FIELD = 'email' #overidding username field in admin login to email
    REQUIRED_FIELDS = ['username'] #for super user

    def __str__(self):
        return self.username
# Create your models here.
