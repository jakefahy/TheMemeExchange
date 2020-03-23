from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbFunctions import getImageByID, addToCart as dbCart

def index(request,image_id): #get actual ID from route
    context = {"image" : getImageByID(image_id)}
    template = loader.get_template('details.html')
    return HttpResponse(template.render(context, request))

def addToCart(request, image_id):
	dbCart(request.user, image_id)
	context = {"image" : getImageByID(image_id)}
	template = loader.get_template('details.html')
	return HttpResponse(template.render(context, request))
