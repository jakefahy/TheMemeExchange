from django.contrib.auth.models import User
from ProfilePage.models import Account

def createUser(username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()
    acct = Account(user=user, memeBucks=0)
    acct.save()
