from django.shortcuts import render
from django.http import HttpResponse
from dbFunctions import getLastTenImg
from django.template import loader
from dbFunctions import getImageByTag, getImageByUser, getCreators

def index(request):
    context = {"images": getLastTenImg()}
    template = loader.get_template('front.html')
    return HttpResponse(template.render(context,request))

def search(request):
    if request.method == 'GET':
        term = request.GET['tag']
        searchOption = request.GET['searchOptions']
        creators = getCreators()
        for creator in creators:
            print(creator)
        if(searchOption == "user"):
            context = {"images": getImageByUser(user)}
        elif(searchOption == "tag"):    
            context = {"images": getImageByTag(term)}
        else:
            context = {"images": getLastTenImg()}
            print("Uh oh this shouldn't happen")
        template = loader.get_template('front.html')
        return HttpResponse(template.render(context,request))
# Create your views here.
