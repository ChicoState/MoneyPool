from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms
from .models import Question, Choice
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block


from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
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

#Login View Basic Profile
@login_required(login_url='/login/')
def index(request):
        if request.user.is_authenticated:
            if request.method == "GET":
                all_trips = models.Event.objects.all().order_by('date')
                tripInvites = models.TripInviteRequest.objects.all()
                attending = models.TripAttendees.objects.all()
                trip_list = []
                trip_invite_list = []
                attending_list = []
                friends_list = []
                fromreqs = 0  # user has received a request
                allFRs = Friend.objects.requests(request.user)
                for f in allFRs:
                    if f.to_user.id == request.user.id:
                        fromreqs += 1

                for e in all_trips:
                    if e.author == request.user:
                        trip_list += [{
                            "location":e.location,
                            "date":e.date,
                            "attendants":e.attendants,
                            "invited":e.invited,
                            "id":e.id
                        }]
                for t in tripInvites:
                    if t.to_user == request.user:
                        trip_invite_list += [{
                            "name":t.tripid.location,
                            "from":t.from_user.username,
                            "tripID": t.tripid.id,
                        }]
                        
                for a in attending:
                    if a.userid.username == request.user.username:
                        attending_list += [{
                            "location": a.tripid.location,
                            "date": a.tripid.date,
                            "id":a.tripid.id
                        }]
                context = {
                    "title":"My Profile",
                    "tripTitle": "My Trips",
                    "attendingTitle": "Trips Attending",
                    "page_name":"Moneypool",
                    "name": request.user.first_name,
                    "data": trip_list,
                    "fromreqs": fromreqs,
                    "tripInvites":trip_invite_list,
                    "attending":attending_list
                }
                return render(request, "profile.html", context=context)
        else:
            return redirect('/login/')

# Profile view for a non-logged-in user
def profile2(request, id):
    if request.user.is_authenticated:
        if request.method == "GET":
            all_users = User.objects.all()
            all_trips = models.Event.objects.all()
            user = ""
            button = ""
            sentreqs = 0  # user has sent a request
            for u in all_users:
                if u.id == id:
                    user = u
                    button = 1
            arefriends = Friend.objects.are_friends(request.user, user) == True
            allFRs = Friend.objects.requests(request.user)
            for f in allFRs:
                if f.from_user.id == id:
                    sentreqs = 1
                if f.to_user.id == id:
                    fromreqs = 1

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
                friends = Friend.objects.friends(request.user)
                invites = request.POST.get("friends", None)
                for f in friends:
                    if f.username in request.POST:
                        status = "about to create request"
                        myrequest = models.TripInviteRequest.objects.create_trip_invite(add_trip, request.user, f)
            else:
                return redirect("/login")
    else:
        form_instance = forms.EventForm()
        friends = Friend.objects.friends(request.user)



    context = {
        "title":"New Trip",
        "page_name":"Moneypool",
        "status":status,
        "form": form_instance,
        "friends":friends
    }
    return render(request, "addtrip.html", context=context)

#Trip details
def tripDetails_view(request, tripID):
    if request.method == "GET":
        if request.user.is_authenticated:
            currUser = request.user
            t = models.Event.objects.get(id=tripID)
            allAttendees = models.TripAttendees.objects.all()
            isattending = 0
            for a in allAttendees:
                if a.userid == request.user:
                    if a.tripid.id == tripID:
                        isattending = 1
            isauthor = 1
            if t.author != request.user:
               isauthor = 0
            
            context = {
                "title": t.location,
                "id": t.id,
                "isauthor": isauthor,
                "isattending": isattending
            }
            return render(request, "tripdetails.html", context=context)
        else:
            return redirect('/login/')

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



#Script to populate tables with users and trips
def populateUsers(request):
    #### USERS ####
    user1 = User.objects.create_user('hpotter', 'hpotter@hogwarts.com', '123!@#123')
    user1.first_name = "Harry"
    user1.last_name = "Potter"
    user1.save()

    user2 = User.objects.create_user('hgranger', 'hgranger@hogwarts.com', '123!@#123')
    user2.first_name = "Hermione"
    user2.last_name = "Granger"
    user2.save()

    user3 = User.objects.create_user('dmalfoy', 'dmalfoy@hogwarts.com', '123!@#123')
    user3.first_name = "Draco"
    user3.last_name = "Malfoy"
    user3.save()

    user4 = User.objects.create_user('rweasley', 'rweasley@hogwarts.com', '123!@#123')
    user4.first_name = "Ronald"
    user4.last_name = "Weasley"
    user4.save()

    return redirect("/login")
     
def populateTrips(request):

    all_users = User.objects.all()
    #### TRIPS ####
    trip1 = models.Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, 0, all_users[0], 1 )
    trip2 = models.Event.objects.create_event("Dumbledoor's Office", "2021-03-20", 0, 0, all_users[0], 1 )
    trip3 = models.Event.objects.create_event("Lavender's House", "2021-03-23", 0, 0, all_users[3], 1 )
    trip4 = models.Event.objects.create_event("The Library", "2021-02-28", 0, 0, all_users[1], 1 )
    trip5 = models.Event.objects.create_event("Hagrid's House", "2021-07-15", 0, 0, all_users[1], 1 )
    trip6 = models.Event.objects.create_event("Snape's Office", "2021-05-28", 0, 0, all_users[2], 1 )

    return redirect("/login")

#function to accept a trip request
def acceptTripReq(request, id):
    userInvites = models.TripInviteRequest.objects.all()
    inviteList = []
    for u in userInvites:
        if u.to_user == request.user:
            if u.tripid.id == id:
               u.accept()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#This is where the suggestion list of the trip is
@login_required(login_url='/login/')
def suggestionIndex(request):
	question_list = models.Question.objects.all().order_by('pub_date')
	context = {
		'latest_question_list': question_list
	}
	return render(request, 'suggestionIndex.html', context=context)

#This is what details are apart of each suggestion
@login_required(login_url='/login/')
def suggestionDetail(request, question_id):
	try:
		queryset = models.Question.objects.get(pk=question_id)
	except models.Question.DoesNotExist:
		raise Http404("Question does not exist")
	return render(request, 'suggestionDetail.html', { 'question': queryset})

#This returns the result of each suggestion
@login_required(login_url='/login/')
def suggestionResults(request, question_id):
	queryset = models.Question.objects.get(pk=question_id)
	return render(request, 'suggestionResults.html', {'question': queryset})

#This is how the user votes on a suggestion
@login_required(login_url='/login/')
def suggestionVote(request, question_id):
	queryset = models.Question.objects.get(pk=question_id)
	try:
		tempVote = queryset.choice_set.get(pk=request.POST['choice'])
	except models.Choice.DoesNotExist:
		return render(request, 'suggestions/suggestionDetail.html', { 'question': queryset})
	finally:
		tempVote.votes += 1
		tempVote.save()
		return HttpResponseRedirect(reverse('suggestions:results', args=(queryset.id,)))
