from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
import json
from django.shortcuts import redirect
from dbFunctions import uploadImagetoDB, getUserCoins, getUserMemes, updateMemeInDB, getMemeById, getUserMemes, uploadImagetoDB
from django.contrib.auth import logout as djangoLogout, login as djangoLogin, authenticate
from django.shortcuts import redirect

def index(request):
    memes = getUserMemes(request.user.id)
    context = {"mymemes" : memes}
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))

def uploadMemeImg(request):
    if request.method == 'POST':

        #Make sure form contained an image
        if not request.FILES:
            messages.add_message(request,20, "Upload Failed - No Image Detected")
            return redirect("/Profile")

        data = request.POST.copy()

        #Make sure user provided tags for post and make a list to hold tags
        if not data.get('FirstTag') and not data.get('SecondTag'):
            messages.add_message(request,20, "Upload Failed - Atleast 2 Tags Required")
            return redirect("/Profile")
        tags = []
        tags.append(data.get('FirstTag'))
        tags.append(data.get('SecondTag'))

        #Check to see if user provided optional tags
        if data.get('ThirdTag'):
            tags.append(data.get('ThirdTag'))
        if data.get('FourthTag'):
            tags.append(data.get('FourthTag'))
        if data.get('FifthTag'):
            tags.append(data.get('FifthTag'))

        #If user didn't provide a description set a default one
        if not data.get('descriptionbox'):
            descript = "No Description Provided"
        descript = data.get('descriptionbox')

        #Grab current user and the image file and save image
        current_user = request.user.id
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)

        #Upload image to firebase and get the url back
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate('the-meme-exchange-026e359fe3e6.json')
            default_app = firebase_admin.initialize_app(cred, {'storageBucket': 'the-meme-exchange.appspot.com'})
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(uploaded_file_url)
        blob.make_public()

        #Clean up local directory of image data
        if blob.public_url:
            fs.delete(filename)

        #Upload image link to our postgres db
        uploadImagetoDB(blob.public_url,tags,descript,current_user)

        #Send toast back to user and refresh page
        messages.add_message(request,20, "A Fine Addition To Your Collection")
        return redirect("/Profile")
    else:
        messages.add_message(request,20, "You Submitted Nothing, Good Job")
        return redirect("/Profile")


def logout(request):
    djangoLogout(request)
    return redirect("/Profile/")

def login(request):
    if request.method == "GET":
        username = request.GET['uname']
        password = request.GET['psw']
        user = authenticate(request, username=username, password=password)
        request.session['coins'] = getUserCoins(user)
        if user is not None:
            djangoLogin(request, user)
        else:
            print("No user found")
        return redirect("/Profile/")


def getMeme(request):
    response = {}
    if request.is_ajax():
        want = request.GET.get('memeid')
        memeQuery = getMemeById(want)
        memeObject = memeQuery[0]
        response['memeLink'] = memeObject.link
        response['memeDescription'] = memeObject.description
        response['memeTags'] = memeObject.tags
        response['id'] = memeObject.id
    return JsonResponse(response)

def updateMeme(request):
    data = request.POST.copy()
    tags = []

    #Make sure user provided tags for post and make a list to hold tags
    if not data.get('FirstTag') and not data.get('SecondTag'):
        messages.add_message(request,20, "Update Failed - Atleast 2 Tags Required")
        return redirect("/Profile")
    tags = []
    tags.append(data.get('FirstTag'))
    tags.append(data.get('SecondTag'))

    #Check to see if user provided optional tags
    if data.get('ThirdTag'):
        tags.append(data.get('ThirdTag'))
    if data.get('FourthTag'):
        tags.append(data.get('FourthTag'))
    if data.get('FifthTag'):
        tags.append(data.get('FifthTag'))

    #If user didn't provide a description set a default one
    if not data.get('descriptionbox'):
        descript = "No Description Provided"
    descript = data.get('descriptionbox')

    id = data.get('imageId')

    updateMemeInDB(tags,descript,id)
    messages.add_message(request,20, "Meme Updated!")

    return redirect("/Profile/")
