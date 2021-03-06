from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import requests
import firebase_admin
from firebase_admin import credentials
import google.cloud
from firebase_admin import storage
import os
import json
from dbFunctions import uploadImagetoDB, getUserCoins, getUserMemes, updateMemeInDB, getMemeById, getUserMemes, uploadImagetoDB, deleteMemefromDB, getOwnedMemes, getFollowers, getFollowing
from django.contrib.auth import logout as djangoLogout, login as djangoLogin, authenticate
from django.shortcuts import redirect
from PIL import Image, ImageFilter, ImageFont, ImageDraw

def index(request):
    if(request.user.is_anonymous):
        return redirect("/createAccount")
    memes = getUserMemes(request.user.id)
    purchased = getOwnedMemes(request.user)
    followers = getFollowers(request.user.id)
    following = getFollowing(request.user.id)
    owned = []
    for m in purchased:
        meme_query = getMemeById(m)
        owned.append(meme_query[0])
    context = {"mymemes" : memes, "ownedmemes" : owned, "followers" : len(followers),
    "following" : len(following)}
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
        current_username = request.user.username
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)


        # if(checkforWatermark(uploaded_file_url)):
        #     messages.add_message(request,20, "Upload Failed - Watermark Detected")
        #     return redirect("/Profile")
        #
        #
        # addWatermark(uploaded_file_url)



        #Upload image to firebase and get the url back
        if (not len(firebase_admin._apps)):
            cred = credentials.Certificate('the-meme-exchange-026e359fe3e6.json')
            default_app = firebase_admin.initialize_app(cred, {'storageBucket': 'the-meme-exchange.appspot.com'})
        bucket = storage.bucket()
        blob = bucket.blob(filename)
        blob.upload_from_filename(uploaded_file_url)
        blob.make_public()

        # if image is gif or something similar, do not blur image
        file_type = uploaded_file_url.split(".")[-1]
        if file_type == ".png" or file_type == "jpg" or file_type == "jpeg":
            im = createBlur(uploaded_file_url)
            im.save("outfile.png")
            blob2 = bucket.blob("blurred_"+filename)
            blob2.upload_from_filename("outfile.png")
            blob2.make_public()
            #Upload image link with blurred image to our postgres db
            uploadImagetoDB(blob.public_url,blob2.public_url,tags,descript,current_username,current_user)
        else:
            #Upload image link with default blur to our postgres db
            default = "http://wallpaperstock.net/wallpapers/thumbs1/42657hd.jpg"
            uploadImagetoDB(blob.public_url,default,tags,descript,current_username,current_user)

        #Clean up local directory of image data
        if blob.public_url:
            fs.delete(filename)
        if blob2.public_url:
            fs.delete("outfile.png")



        #Send toast back to user and refresh page
        messages.add_message(request,20, "A Fine Addition To Your Collection")
        return redirect("/Profile")
    else:
        messages.add_message(request,20, "You Submitted Nothing, Good Job")
        return redirect("/Profile")


def logout(request):
    djangoLogout(request)
    return redirect("/")

def login(request):
    if request.method == "GET":
        username = request.GET['uname']
        password = request.GET['psw']
        user = authenticate(request, username=username, password=password)


        if user is not None:
            djangoLogin(request, user)
            request.session['coins'] = getUserCoins(user)
            return redirect("/Profile/")
        else:
            return redirect("/")
        return redirect("/")


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

def deleteMeme(request):
    data = request.POST.copy()
    id = data.get("deleteId")
    deleteMemefromDB(id)
    messages.add_message(request,20, "Meme Deleted!")
    return redirect("/Profile/")

def createBlur(path):
    im = Image.open(path).filter(ImageFilter.GaussianBlur(200))
    return im


# def addWatermark(path):
#     photo = Image.open(path)
#     text='The-Meme-Exchange'
#
#     # make the image editable
#     drawing = ImageDraw.Draw(photo)
#
#     w, h = photo.size
#
#     pos = (w-150,h-28)
#     font = ImageFont.truetype("arial.ttf", 15)
#     black = (0, 0, 0)
#     drawing.text(pos, text, fill=black, font=font)
#     photo.save()
#
# def checkforWatermark(path):
#     filename = path
#     payload = {'apikey': "31510f9df888957"}
#     with open(filename, 'rb') as f:
#         r = requests.post('https://api.ocr.space/parse/image',
#                           files={filename: f},
#                           data=payload,
#                           )
#
#
#     test = r.content.decode().split(":")
#     #print(test)
#     for i in range(len(test)):
#         #print(test[i])
#         if "ParsedText" in test[i]:
#             line = test[i+1]
#
#
#     if "-Exchange" in line or "Them me" in line or "me-" in line:
#         return True
#     else:
#         return False
