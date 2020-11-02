from django.db import models
from django.contrib.auth.models import User
import datetime
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
#def createEvent():
#    Event.location = input("Where are you going?: ")
#    Event.date = input("When are you going?: ")

