from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from dbFunctions import createUser

from .forms import InsertAcctForm


def index(request):
    context = {}
    template = loader.get_template('createAcct.html')
    return HttpResponse(template.render(context, request))

def insertAcct(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        createUser(username, email, password)
        #login session
        # go to home page
        return HttpResponse("acct created")
