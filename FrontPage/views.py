from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,'front.html')
# Create your views here.