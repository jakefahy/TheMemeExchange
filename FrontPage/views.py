from django.shortcuts import render,redirect
from django.http import HttpResponse
from dbFunctions import getLastTenImg
from django.template import loader
from dbFunctions import getImageByTag, getImageByUser, getCreators, getViewedMemes, getImageByDescription

def index(request):
    if request.user.is_anonymous:
        viewed = []
    else:
        viewed = getViewedMemes(request.user)
    context = {"images": getLastTenImg(), "viewed": viewed}
    template = loader.get_template('front.html')
    return HttpResponse(template.render(context,request))

def searchByTag(request):
    if request.method == 'GET':
        try:
            searchOption = request.GET['searchOptions']
            creators = getCreators()
            #for creator in creators:
            #    print(creator)
            if(searchOption == "user"):
                user = request.GET['tag']
                context = {"images": getImageByUser(user)}
            elif(searchOption == "tag"):
                term = request.GET['tag']
                context = {"images": getImageByTag(term)}
        except:
            context = {"images": getImageByDescription(request.GET['tag'])}
            
        
        template = loader.get_template('front.html')
        return HttpResponse(template.render(context,request))
