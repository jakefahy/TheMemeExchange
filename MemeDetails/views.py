from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from dbFunctions import getImageByID, addToCart as dbCart, getUserByID, getOwnedMemes, getCart

def index(request,image_id): #get actual ID from route
	img = getImageByID(image_id)
	context = {"image" : img, "user" : getUserByID(img.creator), "owned" : getOwnedMemes(request.user), "cart" : getCart(request.user)}
	template = loader.get_template('details.html')
	return HttpResponse(template.render(context, request))

def addToCart(request, image_id):
	dbCart(request.user, image_id)
	img = getImageByID(image_id)
	context = {"image" : img, "user" : getUserByID(img.creator)}
	return redirect("/memeDetails/"+str(image_id))