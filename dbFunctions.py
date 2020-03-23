from django.contrib.auth.models import User
from ProfilePage.models import Account
from ProfilePage.models import ImageLink

def createUser(username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()
    acct = Account(user=user, memeBucks=0)
    acct.save()

def uploadImagetoDB(link):
    img = ImageLink(link=link)
    img.save()

def getImageByID(image_id):
	return ImageLink.objects.get(id=image_id)

def addToCart(currUser, id):
	acct = Account.objects.get(user=currUser)
	acct.cartItems.append(id)
	acct.save()
