from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
	if(request.user.is_anonymous):
		return redirect("/createAccount")
	return render(request,'about.html')
# Create your views here.
