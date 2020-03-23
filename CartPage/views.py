from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbFunctions import getCart, getImagesFromCart

def index(request):
	context = {"cart" : getImagesFromCart(getCart(request.user))}
	template = loader.get_template('cart.html')
	return HttpResponse(template.render(context, request))