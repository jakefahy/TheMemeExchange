from django.contrib.auth.models import User
from ProfilePage.models import Account
from ProfilePage.models import ImageLink

def getLastTenImg():
    q = ImageLink.objects.all()
    return q if len(q) < 10 else q[-10:]

def createUser(username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()
    acct = Account(user=user, memeBucks=0)
    acct.save()

def uploadImagetoDB(link,tags,description,creator):
    img = ImageLink(link=link,tags=tags,description=description,creator=creator)
    img.save()

def getUserCoins(user):
    return Account.objects.get(user=user).memeBucks

def updateUserCoins(user, purchaseAmmt):
    acct = Account.objects.get(user=user)
    acct.memeBucks += purchaseAmmt
    acct.save()
    return acct.memeBucks

def getUserMemes(id):
    query = ImageLink.objects.filter(creator = id)
    return query

def getMemeById(id):
    query = ImageLink.objects.filter(id = id)
    return query

def updateMemeInDB(tags,description,id):
    print(id)
    img = ImageLink.objects.get(id = id)
    img.description = description
    img.tags = tags
    img.save()

def deleteMemefromDB(id):
    img = ImageLink.objects.get(id = id)
    img.delete()
