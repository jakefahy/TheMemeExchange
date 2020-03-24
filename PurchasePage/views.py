from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from dbFunctions import updateUserCoins

def index(request):
    if(request.user.is_anonymous):
        return redirect("/createAccount")
    context = {}
    template = loader.get_template('purchase.html')
    return HttpResponse(template.render(context, request))

def purchase(request):
    if request.method == "POST":
        purchaseAmmt = int(request.POST.get('purchaseAmmt'))
        newAmmt = updateUserCoins(request.user, purchaseAmmt)
        request.session['coins'] = newAmmt
    return JsonResponse({"success": "yes"})
