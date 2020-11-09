from django.db import models
from django.contrib.auth.models import User
import datetime
import secrets

#AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

# Create your models here.
class EventManager(models.Manager):
    def create_event(self, location, date, attendants, invited, author, public ):
        event = self.create(location=location, date=date, attendants=attendants, invited=invited, author=author, public=public)
        return event
    def create_attendee(self, tripid, userid):
        attendee = self.create(tripid=tripid, userid=userid)
        return attendee
    
        
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

class TripAttendees(models.Model):
    tripid = models.ForeignKey(Event, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = EventManager()

class TripInviteRequest(models.Model):
    tripid = models.ForeignKey(Event, on_delete=models.CASCADE)
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trip_requests_sent",
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="trip_requests_received",
    )
    
    def __str__(self):
        return ("%s" % self.from_user)
    
    def accept(self):
        """ Accept this trip request """
        TripAttendees.objects.create_attendee(to_user=self.to_user, tripid=self.tripid)
        self.delete()
        return True


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date Published')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
