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

def remove(img_id,user):
	acct = Account.objects.get(user=user)
	cart = getImagesFromCart(acct.cartItems)
	final = []
	for i in range(len(cart)):
		if (cart[i]).id == img_id:
			cart = cart[:i]+cart[i+1:]
			for j in range(len(cart)):
				final.append(cart[j].id)
			acct.cartItems = final
			acct.save()
			break





