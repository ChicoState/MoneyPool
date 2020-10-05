from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from . import forms
import datetime #for testing mytrips
# Create your views here.

class trips:  
    def __init__(self, name, cost, date):  
        self.name = name  
        self.cost = cost 
        self.date = date.strftime("%m/%d/%Y")
#Login View
@login_required(login_url='/login/')
def index(request):
        if request.user.is_authenticated:
            u = User.objects.get(username=request.user.username)
            mytrips = []
            x = datetime.datetime(2020, 11, 15)
            mytrips.append(trips("Costa Rica", 500, x))
            x = datetime.datetime(2020, 12, 25)
            mytrips.append(trips("Christmas Vacation", 800, x))
            context = {
                "title":"My Profile",
                "page_name":"Moneypool",
                "name": u.first_name,
                "data": mytrips
            }
            return render(request, "profile.html", context=context)
        else:
            return redirect('/login/')



#logout
def logout_view(request):
    logout(request)
    return redirect("/login/")

#registration view
def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

#Add a Trip
def addTrip(request):
    add_trip = forms.addTrip(request)
    context = {
        "title":"New Trip",
        "page_name":"Moneypool",
        "form": add_trip,
    }
    return render(request, "trip.html", context=context)