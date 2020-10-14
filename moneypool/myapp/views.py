from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from . import forms
import datetime #for testing mytrips
# Create your views here.

#Login View
@login_required(login_url='/login/')
def index(request):
        if request.user.is_authenticated:
            if request.method == "GET":
                all_trips = models.Event.objects.all().order_by('date')
                trip_list = []
                friends_list = []
                for e in all_trips:
                    if e.author == request.user:
                        trip_list += [{
                            "location":e.location,
                            "date":e.date,
                            "attendants":e.attendants,
                            "invited":e.invited
                        }]

                
                context = {
                    "title":"My Profile",
                    "page_name":"Moneypool",
                    "name": request.user,
                    "data": trip_list
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
def addTrip_form_view(request):
    status = ""
    if request.method == "POST":
        if request.user.is_authenticated:
            form_instance = forms.EventForm(request.POST)
            if form_instance.is_valid():
                add_trip = form_instance.save(request=request)
                status = "Trip Saved"
        else:
            return redirect("/login")
    else:
        form_instance = forms.EventForm()

    context = {
        "title":"New Trip",
        "page_name":"Moneypool",
        "status":status,
        "form": form_instance,
    }
    return render(request, "addtrip.html", context=context)

#View public and friend trips
@login_required(login_url='/login/')
def viewTrips_view(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            all_trips = models.Event.objects.all().order_by('date')
            public_trips = []
            friends_list = []
            for e in all_trips:
                if e.author != request.user:
                    if e.public == True:
                        public_trips += [{
                            "location":e.location,
                            "author": e.author,
                            "date":e.date,
                            "attendants":e.attendants,
                            "invited":e.invited
                        }]
            context = {
                "title":"Search for A Trip",
                "page_name":"Moneypool",
                "name": request.user,
                "data": public_trips
            }
            return render(request, "searchTrips.html", context=context)
    else:    
        return redirect('/login/')
