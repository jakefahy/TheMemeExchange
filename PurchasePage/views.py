from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from dbFunctions import updateUserCoins

def index(request):
    context = {}
    template = loader.get_template('purchase.html')
    return HttpResponse(template.render(context, request))

def purchase(request):
    if request.method == "POST":
        purchaseAmmt = int(request.POST.get('purchaseAmmt'))
        newAmmt = updateUserCoins(request.user, purchaseAmmt)
        request.session['coins'] = newAmmt
    return JsonResponse({"success": "yes"})
