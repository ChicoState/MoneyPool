from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class Event(models.Model):
    location = models.CharField(max_length = 30)
    date = models.DateField()
    attendants = models.IntegerField()
    #invites = []     Lets wait on this one. Maybe we can normalize tables so no array
    invited = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default = False)

    def __str__(self):
        return self.location + " - " + self.date.strftime("%m/%d/%Y")
#def createEvent():
#    Event.location = input("Where are you going?: ")
#    Event.date = input("When are you going?: ")

class Suggestion(models.Model):
    suggestion = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    dateSuggestion = models.DateField()

    @property
    def get_choice_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.text

class suggestionChoice(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    suggestionChoice = models.CharField(max_length=255)

    @property
    def get_choice_count(self):
        return self.vote_set.count()

    def __str__(self):
        return self.suggestion - self.suggestionChoice

class suggestionVote(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(suggestionChoice, on_delete=models.CASCADE)

    def __str__(self):
        return self.suggestion.text - self.suggestionChoice - self.user
