from django.test import TestCase, Client
from myapp.models import Event, TripAttendees, TripInviteRequest, Question, Choice
from friendship.models import Friend, FriendshipRequest
from django.contrib.auth.models import User

#To run the tests, use the command: python manage.py test myapp/

# Create your tests here.
class EventModelTest(TestCase):
    #Put this function in every test class
    #It is meant to set up the initial test objects
    #It will only run one time, as opposed to every time a test is called
    def setUpTestData():
        print("Setting up Event Tests.")
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
        print("----Test: trip_location.")
        trip1 = Event.objects.get(id=1)
        loc = trip1.location
        self.assertEqual(loc, 'Quittich Pitch')

    #Ensure number invited is stored correctly
    def test_invited(self):
        print("----Test: num_invited")
        trip1 = Event.objects.get(id=1)
        inv = trip1.invited
        self.assertEqual(inv, 0)
    
    #Ensure number of attendees is stored correctly as 1 by default
    def test_attendees(self):
        print("----Test: test_attendees_on_event_create")
        trip1 = Event.objects.get(id=1)
        att = trip1.attendants
        self.assertEqual(att, 1)




    
class Attendee_Tests(TestCase):
    #setup function
    def setUpTestData():
        print("Setting up Attendee Tests.")
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

    #Ensure number of attendees is incremented when someone joins a trip
    def test_attendees(self):
        print("----Test: test_attendees_on_join_trip")
        trip1 = Event.objects.get(id=1)
        att = trip1.attendants

        self.assertEqual(att, 2)

    #Ensure number of attendees in a trip is decremented when someone leaves
    def test_cancel_attendee(self):
        print("----Test: test_attendees_on_leave_trip")
        attendee1 = TripAttendees.objects.get(id=1)
        attendee1.remove(1)
        trip1 = Event.objects.get(id=1)
        self.assertEqual(trip1.attendants, 1)

    #Ensure they are marked to attend the correct trip
    def test_attending_correct_trip(self):
        print("----Test: Is attending correct trip?")
        attendee1 = TripAttendees.objects.get(id=1)
        tripID = attendee1.tripid.id
        self.assertEqual(tripID, 1)

class TripIR_Tests(TestCase):
    #setup function
    def setUpTestData():
        print("Setting up Trip Invite Request Tests.")
        User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        User.objects.create_user(username='rweasley', email='rweasley@hogwarts.com', password='123!@#123')        
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Ron"
        user2.last_name = "Weasley"
        user2.save()
        trip1 = Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        TripInviteRequest.objects.create_trip_invite(trip1, user1, user2)
        pass

    #Tests that the invite request is assigned the correct variables
    def test_assigned_variables_invite_req(self):
        print("----Test: test_assigned_variables_invite_req")
        trip1 = Event.objects.get(id=1)
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        invite1 = TripInviteRequest.objects.get(id=1)
        self.assertEqual(invite1.from_user.id, user1.id)
        self.assertEqual(invite1.to_user.id, user2.id)
        self.assertEqual(invite1.tripid.id, trip1.id)

    
    #Tests that when trip invite request is accepted
    #The request is deleted from the database and a new entry is 
    #Added in Attendees
    def test_accept_request(self):
        print("----Test: test_accept_trip_request")
        invite1 = TripInviteRequest.objects.get(id=1)
        invite1.accept()
        try:
            attendees = TripAttendees.objects.get(id=1)
            print("Attendee added")
        except:
            print("Error: Attendee not added on accept_trip_request")
            self.assertFalse(True)
        
        try:
            invites = TripInviteRequest.objects.get(id=1)
            #if reaches here, invite was not deleted
            print("Error: invite request not deleted")
            self.assertFalse(True)
        except:
            print("There are no invites")
            self.assertTrue(True)

#Test Friends
class Friends(TestCase):
    #setup function
    def setUpTestData():
        print("Setting up Friends tests.")
        User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        User.objects.create_user(username='rweasley', email='rweasley@hogwarts.com', password='123!@#123')        
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Ron"
        user2.last_name = "Weasley"
        user2.save()
        Friend.objects.add_friend(user1, user2)
        pass

    #Tests that the friend request is assigned the correct variables
    def test_assigned_variables(self):
        print("----Test: test_assigned_variables")
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        invite1 = FriendshipRequest.objects.get(id=1)
        self.assertEqual(invite1.from_user.id, user1.id)
        self.assertEqual(invite1.to_user.id, user2.id)


    #Tests that accepted friendships delete from FriendshipRequest
    #and add to Friends model
    def test_accept_friendship(self):
        print("----Test: friendship accept()")
        invite1 = FriendshipRequest.objects.get(id=1)
        invite1.accept()

        #Test friends
        try:
            friendships = Friend.objects.get(id=1)
            #test passed
        except:
            #if reaches here, then test failed
            self.assertTrue(False)
        
        #test no friend requests
        try:
            frs = FriendshipRequests.objects.get(id=1)
            #if reaches here, then test failed
            self.assertTrue(False)
        except:
            #Test passed
            self.assertTrue(True)   

    #Tests that users cannot be friends with themselves
    def test_friends_with_self(self):
        print("----Test: cannot_be_friends_with_themselves")
        user1 = User.objects.get(id=1)
        try:
            Friend.objects.add_friend(user1, user1)
            #If reaches here, then failed test
            print("Error: Failed cannot be friends with themselves")
            self.assertTrue(False)
        except:
            #Test should reach here
            self.assertTrue(True)

    #Tests that users cannot be friends with a friend more than once
    def test_friends_with_friend(self):
        print("----Test: cannot_be_friends_with_a_friend")
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        fr = FriendshipRequest.objects.get(id=1)
        fr.accept()  ##Also tests accept friendship function
        try:
            Friend.objects.add_friend(user1, user2)
            #If reaches here, then failed test
            print("Error: Failed cannot be friends with a friend")
            self.assertTrue(False)
        except:
            #Test should reach here
            self.assertTrue(True)   

    #Tests that users cannot be friends with a friend more than once
    def test_friends_with_requested(self):
        print("----Test: cannot_send_fr_to_requested")
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        fr = FriendshipRequest.objects.get(id=1)
        try:
            Friend.objects.add_friend(user1, user2)
            #If reaches here, then failed test
            print("Error: Failed cannot send multiple friend requests")
            self.assertTrue(False)
        except:
            #Test should reach here
            self.assertTrue(True)   
#Test Questions
class Questions_Choices_Voting(TestCase):
    #setup function
    def setUpTestData():
        print("Setting up Questions tests.")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        evt1 = Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        q = Question.objects.create(question_text="Where are we eating?", end_date="2021-02-28", tripId=evt1, category="Food")
        choice1 = Choice.objects.create(question=q, choice_text="Taco Bell", votes=2,cost=10.20)     
        choice2 = Choice.objects.create(question=q, choice_text="McDonalds", votes=1,cost=9.20)   
        choice3 = Choice.objects.create(question=q, choice_text="Chipotle", votes=3,cost=12.20)            
        pass

    def test_assigned_variables(self):
        print("----Test: test_assigned_variables")
        q1 = Question.objects.get(id=1)          
        self.assertEqual(q1.category, "Food")  #tied to proper category
        self.assertEqual(q1.tripId.id, 1)      #tied to proper trip
        self.assertEqual(q1.question_text, "Where are we eating?") 

    def test_check_choices(self):
        print("----Test: create_choices")
        c1 = Choice.objects.get(id=1) 
        c2 = Choice.objects.get(id=2) 
        c3 = Choice.objects.get(id=3)                 
        self.assertEqual(c1.question.tripId.id, 1)  #tied to proper trip
        self.assertEqual(c2.choice_text, "McDonalds")      #tied to proper trip
        self.assertEqual(str(c3.cost), '12.20') 
        cost = c1.cost + c2.cost + c3.cost
        self.assertEqual(str(cost), '31.60') #test costs

    def test_set_winner(self):
        print("----Test: set_winner")
        c3 = Choice.objects.get(id=3)   
        q1 = Question.objects.get(id=1) 
        q1.updateChoice(c3.choice_text, 3)       
        self.assertEqual(q1.result, "Chipotle")  #set proper winner
        self.assertEqual(q1.resultID, 3) 
           

class Login_Profile_URLs(TestCase):
    def setUpTestData():
        print("Setting up Login and Profile Url tests.")
        User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user1 = User.objects.get(id=1)
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        pass #This is the part that makes the function only run once


    #TEST LOGIN
    def test_correct_login(self):
        print("----Test: testing correct login")
        c = Client()
        response = c.post('/login/', {'username':'hpotter', 'password': '123!@#123'}, follow=True)
        success = c.login(username='hpotter', password='123!@#123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(success, True)

    def test_incorrect_login_username(self):
        print("----Test: test incorrect login username")
        c = Client()
        success = c.login(username='hgranger', password='123!@#123')
        self.assertEqual(success, False)

    def test_incorrect_login_password(self):
        print("----Test: test incorrect login password")
        c = Client()
        success = c.login(username='hpotter', password='123!@#122')
        self.assertEqual(success, False)

    #Test content passed to view based on logged in user
    def test_correct_profile_content(self):
        print("----Test: test correct profile content")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/profile/')
        result = response.context['data']
        self.assertEqual(result[0]['location'], "Quittich Pitch")
    