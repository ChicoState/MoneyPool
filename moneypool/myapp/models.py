from django.db import models
from django.contrib.auth.models import User
import datetime
import secrets

# Create your models here.
class EventManager(models.Manager):
    def create_event(self, location, date, attendants, invited, author, public ):
        event = self.create(location=location, date=date, attendants=attendants, invited=invited, author=author, public=public)
        return event
        
class Event(models.Model):
    location = models.CharField(max_length = 30)
    date = models.DateField()
    attendants = models.IntegerField()
    #invites = []     Lets wait on this one. Maybe we can normalize tables so no array
    invited = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default = False)
    
    objects = EventManager()
    def __str__(self):
        return self.location + " - " + self.date.strftime("%m/%d/%Y")

class Attendees(models.Model):
    tripid = models.ForeignKey(Event, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

class Invites(models.Model):
    tripid = models.ForeignKey(Event, on_delete=models.CASCADE)
    invitedId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invited_user")
    fromId = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sent_invite")
    



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date Published')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
