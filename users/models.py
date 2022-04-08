from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)  # для ВК
    email = models.EmailField(max_length=128, blank=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def safe_delete(self):
        self.is_active = False
        self.save()

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class ShopUserProfile(models.Model):
    FAT = 'F'
    SLIM = 'S'
    POWER_CHOICES = (
        (FAT, 'Толстый'),
        (SLIM, 'Тонкий'),
    )
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    powerness = models.CharField(verbose_name='мощь', max_length=1, choices=POWER_CHOICES, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
