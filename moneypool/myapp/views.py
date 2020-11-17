from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms
from .models import Question, Choice
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
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
					"name": request.user.first_name,
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

def addSuggestion(request, question_id):
	queryset = models.Choice.objects.all()
	queryset2 = models.Question.objects.get(id=question_id)
	question_set = []
	for e in queryset:
		if e.question.id == question_id:
			if e.question.tripId.author == request.user:
				question_set += [{
					"Suggestion":e.question.question_text,
					"Choices": e.choice_text,
					"Author": e.question.id,
					"choice_text": e.choice_text,
				}]
	context = {
		"Data": question_set,
		"question": queryset2,
	}
	return render(request, 'suggestionDetail.html', context=context)
