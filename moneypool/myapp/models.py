from django.db import models
import datetime
# Create your models here.
        
class Event:
    location = "string"
    date = datetime.datetime.now()
    attendants = 0
    invites = []
    invited = 0

def createEvent():
    Event.location = input("Where are you going?: ")
    Event.date = input("When are you going?: ")