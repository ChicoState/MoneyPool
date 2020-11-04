from django.db import models
from django.contrib.auth.models import User
import datetime
import secrets

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

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date Published')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
