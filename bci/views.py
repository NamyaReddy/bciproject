from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse,JsonResponse
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.utils.cache import add_never_cache_headers


def home(request):
    return render(request,'home.html')
'''
@never_cache
def home(request):
    if (request.method)=="POST":
        name=request.POST['username']
        password=request.POST['password']
        det = { 'name':name,'password':password }
        token = requests.post("https://sport-resources-booking-api.herokuapp.com/AdminLogin",det)
        global p
        p = token.json()['access_token']
        return redirect('home')
        if(p=="Invalid credentials"):
            context={'data':"INVALID CREDENTIALS"}
            return render(request,'login1.html',context)
            return HttpResponse(p)
        else:
            data = requests.get("https://sport-resources-booking-api.herokuapp.com/ResourcesPresent", headers = {'Authorization':f'Bearer {p}'}) 
            res = data.json()
            context={'data': res,}
            return redirect('resources')
    elif (request.method)=="GET":
        if(p):
            if(p=="Invalid credentials"):
                print('invalid')
                context={'data':"INVALID CREDENTIALS"}
                return render(request,'login1.html',context)
            #return HttpResponse(p)
            else:
                print('valid')
                data = requests.get("https://sport-resources-booking-api.herokuapp.com/ResourcesPresent", headers = {'Authorization':f'Bearer {p}'}) 
                res = data.json()
                context={'data': res,}
                return redirect('resources')
        else:
            return redirect('login')

'''