from django.http import HttpResponse
from django.shortcuts import render

def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>Hello World</h1>")