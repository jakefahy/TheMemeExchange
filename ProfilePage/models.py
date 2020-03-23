from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    memeBucks = models.IntegerField(default=0)
    cartItems = ArrayField(models.IntegerField(default=0), blank=True, default=list)

    def __str__(self):
        return self.user.username
