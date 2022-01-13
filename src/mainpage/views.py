from django.shortcuts import render

from tools.migration import Migration

# Create your views here.

def index(request):
    return render(request, 'mainpage/index.html')