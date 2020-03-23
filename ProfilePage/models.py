from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    memeBucks = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class ImageLink(models.Model):
    link = models.TextField(default="AAAAAAAAA")


    def __str__(self):
        return self.link
