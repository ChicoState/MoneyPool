from django.shortcuts import render
from . import models
#from . import forms

# Create your views here.
def index(request):
    return render(request, "base.html")