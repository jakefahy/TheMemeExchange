from django.shortcuts import render
from django.http import HttpResponse
from dbFunctions import getLastTenImg
from django.template import loader
from dbFunctions import getImageByTag

def index(request):
    context = {"images": getLastTenImg()}
    template = loader.get_template('front.html')
    return HttpResponse(template.render(context,request))

def search(request):
    if request.method == 'GET':
        term = request.GET['tag']
        context = {"images": getImageByTag(term)}
        template = loader.get_template('front.html')
        return HttpResponse(template.render(context,request))
# Create your views here.
