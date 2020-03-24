from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbFunctions import getCart, getImagesFromCart, remove, addToPurchased, updateUserCoins, getUserByID, likeImage
from django.shortcuts import redirect

def index(request):
	cart = getImagesFromCart(getCart(request.user))
	context = {"cart" : cart, "total" : len(cart)*10}
	template = loader.get_template('cart.html')
	return HttpResponse(template.render(context, request))

def removeItemFromCart(request, img_id):
	context = {"cart" : getImagesFromCart(getCart(request.user))}
	remove(img_id, request.user)
	return redirect("/shoppingCart")

def purchaseMeme(request):
	cart = getImagesFromCart(getCart(request.user))

	for pic in cart:
		addToPurchased(request.user,pic.id)
		currAmt = updateUserCoins(request.user,-10)
		updateUserCoins(getUserByID(pic.creator),10)
		request.session['coins'] = currAmt
		likeImage(pic.id)
		remove(pic.id,request.user)

	return redirect("/Profile")
