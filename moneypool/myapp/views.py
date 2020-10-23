from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block

#from . import forms
import datetime #for testing mytrips
# Create your views here.

def sendFR(request, id):
    ctx = {"to_username": to_username}

    if request.method == "POST":
        to_user = user_model.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as e:
            ctx["errors"] = ["%s" % e]
        else:
            return redirect("friendship_request_list")

    return render(request, template_name, ctx)

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
                    "tripTitle": "My Trips",
                    "page_name":"Moneypool",
                    "name": request.user.first_name,
                    "data": trip_list
                }
                return render(request, "profile.html", context=context)
        else:    
            return redirect('/login/')

def profile2(request, id):
    if request.user.is_authenticated:
        if request.method == "GET":
            all_users = User.objects.all()
            all_trips = models.Event.objects.all().order_by('date')
            user = ""
            button = ""
            sentreqs = 0
            for u in all_users:
                if u.id == id:
                    user = u
                    button = 1
            arefriends = Friend.objects.are_friends(request.user, user) == True
            allFRs = Friend.objects.requests(request.user)
            for f in allFRs:
                if f.from_user.id == id:
                    sentreqs = 1

            trip_list = []
            for e in all_trips:
                if e.author == user:
                    trip_list += [{
                        "location":e.location,
                        "date":e.date,
                        "attendants":e.attendants,
                        "invited":e.invited
                    }]

            
            context = {
                "title":user.username,
                "tripTitle": user.first_name + "'s Trips",
                "page_name":"Moneypool",
                "name": user.first_name,
                "data": trip_list, 
                "button": button,
                "from": request.user.id,
                "to" : user.username,
                "arefriends" : arefriends,
                "sentreqs" : sentreqs

            }
            return render(request, "profile.html", context=context)

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

def findUsers(request):
    if request.method == "GET":
        all_users = User.objects.all()
        user_list = []
        for u in all_users:
            if u.username != request.user.username:
                user_list += [{
                    "username": u.username,
                    "first_name": u.first_name,
                    "last_name": u.last_name,
                    "id": u.id
                }]
        context = {
            "title": "Find Users",
            "page_name": "MoneyPool",
            "user_list": user_list
        }
        return render(request, "findUsers.html", context=context)
