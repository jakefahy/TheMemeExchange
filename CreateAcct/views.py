from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbFunctions import createUser
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .forms import InsertAcctForm


def index(request):
    context = {"error": "no"}
    template = loader.get_template('createAcct.html')
    return HttpResponse(template.render(context, request))

def insertAcct(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        try:
            createUser(username, email, password)
        except:
            template = loader.get_template('createAcct.html')
            return HttpResponse(template.render({
            "error" : "yes"
            }, request))
        user = authenticate(request, username=username, password=password)
        login(request, user)
        # go to home page
        #return HttpResponse("acct created")
        return redirect("/Profile/")
        #return HttpResponseRedirect('Profile')
