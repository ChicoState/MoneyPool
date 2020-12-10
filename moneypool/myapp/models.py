from django.db import models
from django.contrib.auth.models import User
import datetime
import secrets
from myapp.exceptions import alreadyAttending, alreadyInvited

#AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")

# Create your models here.
class EventManager(models.Manager):
    def create_event(self, location, date, attendants, invited, author, public ):
        event = self.create(location=location, date=date, attendants=attendants, invited=invited, author=author, public=public)
        return event
    def create_attendee(self, tripid, userid):
        allattendees = TripAttendees.objects.all()
        for a in allattendees:
            if a.tripid.id == tripid.id:
                if a.userid.id == userid.id:
                    error = "The user '" + userid.username + "' is already attending trip '" + tripid.location + "'"
                    raise alreadyAttending(error)
        attendee = self.create(tripid=tripid, userid=userid)
        tripid.attendants += 1
        tripid.save()
        return attendee
    def create_trip_invite(self, tripid, from_user, to_user):
        allinvites = TripInviteRequest.objects.all()
        for a in allattendees:
            if a.tripid.id == tripid.id:
                if a.to_user.id == to_user.id:
                    error = "The user '" + userid.username + "' has already been invited on trip '" + tripid.location + "'"
                    raise alreadyinvited(error)
        invite = self.create(tripid=tripid, from_user=from_user, to_user=to_user)
        return invite



class Event(models.Model):
    title = models.CharField(max_length = 30)
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

    def __str__(self):
        return self.tripid.location + "  -  " + self.userid.username

    def remove(self, id):
        trip = Event.objects.get(pk=id)
        trip.attendants -= 1
        trip.save()
        self.delete()

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

    objects = EventManager()

    def __str__(self):
        return self.tripid.location + " - " + self.to_user.username

    def accept(self):
        """ Accept this trip request """
        TripAttendees.objects.create_attendee(self.tripid, self.to_user)
        self.delete()
        return True


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    end_date = models.DateTimeField(null=True, blank=True)
    tripId = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, default = "")
    result = models.CharField(max_length=30, default = "")
    resultID = models.IntegerField(default=0)
    objects = EventManager()

    def updateChoice(self, choice, id):
        self.result = choice
        self.resultID = id
        self.save()
        return True

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    objects = EventManager()
