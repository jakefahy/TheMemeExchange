from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from PIL import Image
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import os
from django.shortcuts import redirect
from dbFunctions import uploadImagetoDB
from django.contrib.auth import logout as djangoLogout, login as djangoLogin, authenticate
from django.shortcuts import redirect

def index(request):
    context = {}
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))

def uploadMemeImg(request):
    if request.method == 'POST':
        if not request.FILES:
            messages.add_message(request,20, "Upload Failed - No Image Detected")
            return redirect("/Profile")
        data = request.POST.copy()
        if not data.get('FirstTag') and not data.get('SecondTag'):
            messages.add_message(request,20, "Upload Failed - Atleast 2 Tags Required")
            return redirect("/Profile")
        tags = []
        tags.append(data.get('FirstTag'))
        tags.append(data.get('SecondTag'))
        if data.get('ThirdTag'):
            tags.append(data.get('ThirdTag'))
        if data.get('FourthTag'):
            tags.append(data.get('FourthTag'))
        if data.get('FifthTag'):
            tags.append(data.get('FifthTag'))
        print(tags)
        if not data.get('descriptionbox'):
            descript = "No Description Provided"
        descript = data.get('descriptionbox')
        print(descript)
        current_user = request.user.id
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)
        print(uploaded_file_url)
        cred = credentials.Certificate('the-meme-exchange-026e359fe3e6.json')
        default_app = firebase_admin.initialize_app(cred, {'storageBucket': 'the-meme-exchange.appspot.com'})
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(uploaded_file_url)
        blob.make_public()
        if blob.public_url:
            fs.delete(filename)
        uploadImagetoDB(blob.public_url,tags,descript,current_user)
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
        if user is not None:
            djangoLogin(request, user)
        else:
            print("No user found")
        return redirect("/Profile/")
