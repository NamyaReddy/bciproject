from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse,JsonResponse
import requests
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.utils.cache import add_never_cache_headers


def home(request):
    return render(request,'home.html')
