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

def index(request):
    context = {}
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))

def uploadMemeImg(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # fs = FileSystemStorage()
        # filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.path(filename)
        # print(uploaded_file_url)
        # cred = credentials.Certificate('the-meme-exchange-026e359fe3e6.json')
        # default_app = firebase_admin.initialize_app(cred, {'storageBucket': 'the-meme-exchange.appspot.com'})
        # bucket = storage.bucket()
        # blob = bucket.blob(filename)
        # blob.upload_from_filename(uploaded_file_url)
        # blob.make_public()
        #
        # if blob.public_url:
        #     fs.delete(filename)

        messages.add_message(request,20, "A Fine Addition To Your Collection")

        return redirect("/Profile")
