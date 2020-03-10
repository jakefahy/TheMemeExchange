from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    #user = models.OneToOneField(User)
    username = models.CharField(max_length=50)
    memeBucks = models.IntegerField(default=0)

    def __str__(self):
        return self.username
