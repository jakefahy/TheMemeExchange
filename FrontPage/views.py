from django.shortcuts import render
from django.http import HttpResponse
from dbFunctions import getLastTenImg
from django.template import loader

def index(request):
    context = {"images": getLastTenImg()}
    template = loader.get_template('front.html')
    return HttpResponse(template.render(context,request))
# Create your views here.
