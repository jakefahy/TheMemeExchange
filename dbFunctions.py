from django.contrib.auth.models import User
from ProfilePage.models import Account
from ProfilePage.models import ImageLink

def getLastTenImg():
    q = ImageLink.objects.order_by('-pub_date')[:40]
    return q


def createUser(username, email, password):
    user = User.objects.create_user(username, email, password)
    user.save()
    acct = Account(user=user, memeBucks=0)
    acct.save()

def uploadImagetoDB(link,blurred,tags,description,username,creator_id):
    img = ImageLink(link=link,blurred=blurred,tags=tags,description=description,creator=creator_id,username=username)
    img.save()
    user = User.objects.get(id=creator)
    acct = Account.objects.get(user=user)
    acct.viewed.append(img.id)
    acct.save()

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
    return ImageLink.objects.filter(creator = id)

def getOwnedMemes(user):
    return Account.objects.get(user=user).purchased

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

def addToPurchased(user,img_id):
	acct = Account.objects.get(user=user)
	acct.purchased.append(img_id)
	acct.save()

def getMemeById(id):
    query = ImageLink.objects.filter(id = id)
    return query

def updateMemeInDB(tags,description,id):
    print(id)
    img = ImageLink.objects.get(id = id)
    img.description = description
    img.tags = tags
    img.save()

def getImageByTag(tag):
    query = ImageLink.objects.all()
    results = []
    for meme in query:
        for memeTag in meme.tags:
            if tag == memeTag:
                results.append(meme)
    return results

def likeImage(imageId):
    img = ImageLink.objects.get(id=imageId)
    img.likes += 1
    img.save()

def deleteMemefromDB(id):
    img = ImageLink.objects.get(id = id)
    img.delete()

def getViewedMemes(user):
    q = Account.objects.get(user=user).viewed
    print(q)
    return q
