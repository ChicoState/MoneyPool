from django.test import TestCase
from myapp.models import Event, TripAttendees
from django.contrib.auth.models import User

#To run the tests, use the command: python manage.py test myapp/

# Create your tests here.
class EventModelTest(TestCase):
    #Put this function in every test class
    #It is meant to set up the initial test objects
    #It will only run one time, as opposed to every time a test is called
    def setUpTestData():
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user1 = User.objects.get(id=1)
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        pass #This is the part that makes the function only run once

    #All test functions go below here.... 
    #Each function must start with the word 'test' or it wont work


    #Ensure trip location is stored correctly
    def test_trip_location(self):
        print("Method: trip_location.")
        trip1 = Event.objects.get(id=1)
        loc = trip1.location
        self.assertEqual(loc, 'Quittich Pitch')

    #Ensure number invited is stored correctly
    def test_invited(self):
        print("Method: num_invited")
        trip1 = Event.objects.get(id=1)
        inv = trip1.invited
        self.assertEqual(inv, 0)
    
    #Ensure number of attendees is stored correctly as 1 by default
    def test_attendees(self):
        print("Method: test_attendees")
        trip1 = Event.objects.get(id=1)
        att = trip1.attendants
        self.assertEqual(att, 1)


    
class Attendee_Tests(TestCase):
    #Put this function in every test class
    #It is meant to set up the initial test objects
    #It will only run one time, as opposed to every time a test is called
    def setUpTestData():
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        User.objects.create_user(username='hgranger', email='hgranger@hogwarts.com', password='123!@#123')
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        event1 = Event.objects.get(id=1)
        TripAttendees.objects.create_attendee(event1, user2)
        pass

    #All test functions go below here.... 
    #Each function must start with the word 'test' or it wont work

    #Ensure number of attendees is incremented when someone joins a trip
    def test_attendees(self):
        print("Method: test_attendees")
        trip1 = Event.objects.get(id=1)
        att = trip1.attendants
        self.assertEqual(att, 2)