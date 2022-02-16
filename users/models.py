from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)