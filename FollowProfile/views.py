from django.shortcuts import render, redirect
from django.http import HttpResponse,  JsonResponse
from dbFunctions import getFollowing, getFollowers, getUserByID, getUserMemes, followUser, checkIfFollowing, unfollow, getViewedMemes, addToViewed
from django.template import loader

def index(request, userID):
	if(request.user.is_anonymous):
		return redirect("/createAccount")
	account = getUserByID(userID)
	followers = getFollowers(account.id)
	following = getFollowing(account.id)
	isFollowing = checkIfFollowing(request.user, followers)
	context = {"id" : userID, "user" : account.username, "followers" : len(followers),
	"following" : len(following), "images" : getUserMemes(account.id), 
	"isFollowing" : isFollowing, "viewed" : getViewedMemes(request.user)}
	template = loader.get_template('otherprofile.html')

	return HttpResponse(template.render(context, request))

def userfollow(request, userID):
	followUser(request.user, userID)
	return redirect('/follow/' + userID)

def userunfollow(request, userID):
	unfollow(request.user, userID)
	return redirect('/follow/' + userID)

def unlockM(request, userID):
    if request.is_ajax():
        id = request.POST.get('memeid')
        creator = request.POST.get('creator')
        status = addToViewed(request.user, id, creator)
        if status != -1:
            request.session['coins'] = status
        return JsonResponse({"status":status})

