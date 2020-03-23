from django.contrib import admin

from .models import Account
from .models import ImageLink

admin.site.register(Account)
admin.site.register(ImageLink)
