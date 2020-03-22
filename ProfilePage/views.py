from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout as djangoLogout, login as djangoLogin, authenticate
from django.shortcuts import redirect

def index(request):
    context = {}
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(context, request))

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
