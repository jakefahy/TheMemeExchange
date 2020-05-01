from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone



class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    memeBucks = models.IntegerField(default=0)
    viewed = ArrayField(models.IntegerField(default=0), blank=True, default=list)
    cartItems = ArrayField(models.IntegerField(default=0), blank=True, default=list)
    purchased = ArrayField(models.IntegerField(default=0), blank=True, default=list)

    def __str__(self):
        return self.user.username

class ImageLink(models.Model):
    link = models.TextField(default="AAAAAAAAA")
    blurred = models.TextField(default="http://wallpaperstock.net/wallpapers/thumbs1/42657hd.jpg")
    tags = ArrayField(models.TextField(max_length=25), blank=True)
    description = models.TextField(default="No Description Provided")
    username = models.TextField(default="Its Over I Have The High Ground")
    creator = models.IntegerField(default=-1)
    likes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published', default=timezone.now)
