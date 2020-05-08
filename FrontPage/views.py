from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from dbFunctions import getLastTenImg
from django.template import loader
from dbFunctions import getImageByTag, getImageByUser, getCreators, getViewedMemes, getImageByDescription, addToViewed

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

def unlock(request):
    if request.is_ajax():
        id = request.POST.get('memeid')
        creator = request.POST.get('creator')
        status = addToViewed(request.user, id, creator)
        if status != -1:
            request.session['coins'] = status
        return JsonResponse({"status":status})
