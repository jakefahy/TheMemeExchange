from django.shortcuts import render
from django.http import HttpResponse
from dbFunctions import getLastTenImg
from django.template import loader
from dbFunctions import getImageByTag, getViewedMemes

def index(request):
    if request.user.is_anonymous:
        viewed = []
    else:
        viewed = getViewedMemes(request.user)
    context = {"images": getLastTenImg(), "viewed": viewed}
    template = loader.get_template('front.html')
    return HttpResponse(template.render(context,request))

def search(request):
    if request.method == 'GET':
        if request.user.is_anonymous:
            viewed = []
        else:
            viewed = getViewedMemes(request.user)
        term = request.GET['tag']
        context = {"images": getImageByTag(term), "viewed": viewed}
        template = loader.get_template('front.html')
        return HttpResponse(template.render(context,request))
