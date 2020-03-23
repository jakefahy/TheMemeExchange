from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbFunctions import getCart, getImagesFromCart, remove
from django.shortcuts import redirect

def index(request):
	context = {"cart" : getImagesFromCart(getCart(request.user))}
	template = loader.get_template('cart.html')
	return HttpResponse(template.render(context, request))

def removeItemFromCart(request, img_id):
	context = {"cart" : getImagesFromCart(getCart(request.user))}
	remove(img_id, request.user)
	return redirect("/shoppingCart")
