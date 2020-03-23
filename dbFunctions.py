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

def getImageByID(image_id):
	return ImageLink.objects.get(id=image_id)

def addToCart(currUser, id):
	acct = Account.objects.get(user=currUser)
	acct.cartItems.append(id)
	acct.save()

def getUserByID(id):
	return User.objects.get(id=id)

def getCart(user):
	return Account.objects.get(user=user).cartItems

def getImagesFromCart(img_ids):
	return [ImageLink.objects.get(id=i) for i in img_ids]

def getUserMemes(id):
    query = ImageLink.objects.filter(creator = id)
    return query
