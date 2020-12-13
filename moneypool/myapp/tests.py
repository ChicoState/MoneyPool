from django.test import TestCase, Client
from myapp.models import Event, TripAttendees, TripInviteRequest, Question, Choice
from friendship.models import Friend, FriendshipRequest
from django.contrib.auth.models import User
from datetime import datetime

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

    def tearDown(self):
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        Friend.objects.remove_friend(user1, user2)

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
        q = Question.objects.create(question_text="Where are we eating?", tripId=evt1, category="Food")
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

    def test_cant_access_profile(self):
        print("----Test: testing unlogged in user trying to access profile")
        c = Client()
        response = c.get('/profile/')
        self.assertEqual(response.status_code, 302) #redirected to login

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
        mytrips = response.context['data']
        first_name = response.context['name']
        friend_reqs = response.context['fromreqs']
        attending_list = response.context['attending']
        self.assertEqual(mytrips[0]['location'], "Quittich Pitch")
        self.assertEqual(first_name, "Harry")
        self.assertFalse(friend_reqs)
        self.assertFalse(attending_list)


    
class Profile_view(TestCase):
    def setUpTestData():
        print("Setting up Profile Url tests.")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username="hgranger", email="hgranger@hogwarts.com", password='123!@#123')
        user3 = User.objects.create_user(username="rweasley", email="rweasley@hogwarts.com", password='123!@#123')        
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        user3.first_name = "Ron"
        user3.last_name = "Weasley"
        user3.save()
        event1 = Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user2, 1 )
        event2 = Event.objects.create_event("Snape's Office", "2021-06-20", 0, user3, 1 )
        TripAttendees.objects.create_attendee(event1, user1)   
        Friend.objects.add_friend(user2, user1)
        TripInviteRequest.objects.create_trip_invite(event2, user3, user1)
        pass #This is the part that makes the function only run once    

    #Test content passed to view based on logged in user
    def test_correct_profile_content(self):
        print("----Test: test correct profile content")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/profile/')
        mytrips = response.context['data']
        first_name = response.context['name']
        friend_reqs = response.context['fromreqs']
        attending_list = response.context['attending']
        trip_invites = response.context['tripInvites']
        self.assertFalse(mytrips)
        self.assertEqual(first_name, "Harry")
        self.assertTrue(friend_reqs)
        self.assertTrue(attending_list)  
        self.assertEqual(attending_list[0]["location"], "Quittich Pitch")  
        self.assertTrue(trip_invites)
        self.assertEqual(trip_invites[0]["name"], "Snape's Office")  
    
    #Test content passed to another users view not friends
    def test_correct_other_profile_content(self):
        print("----Test: test correct profile content for non-logged in user")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/profile/2')
        trips = response.context['data']
        first_name = response.context['name']
        arefriends = response.context['arefriends']
        self.assertFalse(arefriends)
        self.assertTrue(trips)
        self.assertEqual(trips[0]["location"], "Quittich Pitch")
        self.assertEqual(first_name, "Hermione")

class Trip_Details_View(TestCase):
    def setUpTestData():
        print("Setting up Trip_Details_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username="hgranger", email="hgranger@hogwarts.com", password='123!@#123')
        user3 = User.objects.create_user(username="rweasley", email="rweasley@hogwarts.com", password='123!@#123')        
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        user3.first_name = "Ron"
        user3.last_name = "Weasley"
        user3.save()
        event1 = Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user2, 1 )
        pass #This is the part that makes the function only run once            

     #Test content passed to trip_details view
    def test_correct_content(self):
        print("----Test: test correct trip content right after trip creation")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/tripdetails/1/')
        title = response.context['title']
        attendants = response.context['attendeesCount']
        isauthor = response.context['isauthor']
        self.assertFalse(isauthor)
        self.assertEqual(title, "Quittich Pitch")
        self.assertEqual(attendants, 1)  

    #Ensure correct attendee count on page when someone joins a trip
    def test_correct_content_2(self):
        print("----Test: test correct attendee count")
        event1 = Event.objects.get(id=1)
        user1 = User.objects.get(id=1)
        TripAttendees.objects.create_attendee(event1, user1)   
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/tripdetails/1/')
        attendants = response.context['attendeesCount']
        self.assertEqual(attendants, 2)  

    #Ensure trip owner is correct (to show link to invite friends)
    def test_correct_content_3(self):
        print("----Test: test owner of the trip")
        c = Client()
        success = c.login(username='hgranger', password='123!@#123')
        response = c.get('/tripdetails/1/')
        attendants = response.context['attendeesCount'] 
        isauthor = response.context['isauthor']
        self.assertTrue(isauthor)        

class Search_Users_View(TestCase):
    def setUpTestData():
        print("Setting up Search_Users_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username="hgranger", email="hgranger@hogwarts.com", password='123!@#123')
        user3 = User.objects.create_user(username="rweasley", email="rweasley@hogwarts.com", password='123!@#123')        
        user4 = User.objects.create_user(username="dmalfoy", email="dmalfoy@hogwarts.com", password='123!@#123')
        user5 = User.objects.create_user(username="adumbeldoor", email="adumbeldoor@hogwarts.com", password='123!@#123')        
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        user3.first_name = "Ron"
        user3.last_name = "Weasley"
        user3.save()
        user4.first_name = "Draco"
        user4.last_name = "Malfoy"
        user4.save()
        user5.first_name = "Albus"
        user5.last_name = "Dumbeldoor"
        user5.save()
        pass

    def test_check_users(self):
        print("----Test: test all users show up except logged in user")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/findUsers/')
        userlist = response.context['user_list'] 
        self.assertEqual(len(userlist), 4)


class Find_Trips_View(TestCase):
    def setUpTestData():
        print("Setting up Search_Users_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username="hgranger", email="hgranger@hogwarts.com", password='123!@#123')
        user3 = User.objects.create_user(username="rweasley", email="rweasley@hogwarts.com", password='123!@#123')        
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        user3.first_name = "Ron"
        user3.last_name = "Weasley"
        user3.save()
        Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        Event.objects.create_event("Astronomy Tower", "2021-04-20", 0, user2, 0 )
        Event.objects.create_event("Gryffindoor Commonroom", "2021-04-20", 0, user3, 0 )
        Event.objects.create_event("Snape's Office", "2021-04-20", 0, user2, 1 )
        Event.objects.create_event("Lupin's Office", "2021-04-20", 0, user1, 1 )
        Event.objects.create_event("Hagrid's House", "2021-04-20", 0, user3, 1 )
        pass

    def test_check_public_trips(self):
        print("----Test: test all public trips show up not from user")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/viewtrips/')
        triplist = response.context['data'] 
        self.assertEqual(len(triplist), 2) #only 2 trips not from user are public

class Category_Page_View(TestCase):
    def setUpTestData():
        print("Setting up Category_Page_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username="hgranger", email="hgranger@hogwarts.com", password='123!@#123')
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        pass

    def test_check_owner_view(self):
        print("----Test: test owner can add suggestions")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/tripdetails/1/categoryPage/1/') #traveling
        category = response.context['catTitle'] 
        tripName = response.context['name']
        isowner = response.context['owner']
        self.assertEqual(tripName, "Quittich Pitch") 
        self.assertEqual(category, "Traveling")
        self.assertTrue(isowner)

    def test_check_not_owner_view(self):
        print("----Test: test non-owner cannot add suggestions")
        c = Client()
        success = c.login(username='hgranger', password='123!@#123')
        response = c.get('/tripdetails/1/categoryPage/1/') #traveling
        category = response.context['catTitle'] 
        tripName = response.context['name']
        isowner = response.context['owner']
        self.assertEqual(tripName, "Quittich Pitch") 
        self.assertEqual(category, "Traveling")
        self.assertFalse(isowner)

class Add_Trip_Form_View(TestCase):
    def setUpTestData():
        print("Setting up Add_Trip_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username="hgranger", email="hgranger@hogwarts.com", password='123!@#123')
        user3 = User.objects.create_user(username="rweasley", email="rweasley@hogwarts.com", password='123!@#123')        
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()
        user3.first_name = "Ron"
        user3.last_name = "Weasley"
        user3.save()
        fr1 = Friend.objects.add_friend(user1, user2)
        fr2 = Friend.objects.add_friend(user1, user3)
        fr1.accept()
        fr2.accept()
        pass

    def test_check_friends_display(self):
        print("----Test: check that all user's friends are displayed to invite")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/addtrip/')
        friends = response.context['friends'] 
        self.assertEqual(len(friends), 2)

    #Tests the create_trip form as well as inviting friends on a new trip
    def test_form_works(self):
        print("----Test: check that all user's friends are displayed to invite")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.post('/addtrip/', {"location":"home", "date_month": "1", "date_day": "1", "date_year": "2022", "public": "on", "hgranger": "hgranger"})
        response2 = c.get('/profile/')
        tir = TripInviteRequest.objects.get(id=1)
        trips = response2.context['data'] 
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0]["location"], "home")
        self.assertEqual(tir.tripid.location, "home")
        self.assertEqual(tir.from_user.id, 1)
        self.assertEqual(tir.to_user.id, 2)
    

    def tearDown(self):
        user1 = User.objects.get(id=1)
        user2 = User.objects.get(id=2)
        user3 = User.objects.get(id=3)
        Friend.objects.remove_friend(user1, user2)
        Friend.objects.remove_friend(user1, user3)

class Join_Trip_View(TestCase):
    def setUpTestData():
        print("Setting up Join_Trip_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username='hgranger', email='hgranger@hogwarts.com', password='123!@#123')
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()       
        Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        pass

    def test_join_trip(self):
        print("----Test: check that users can successfully join a public trip")
        c = Client()
        success = c.login(username='hgranger', password='123!@#123')
        response = c.post('/joinTrip/1/') 
        attendees = TripAttendees.objects.get(id=1)
        self.assertTrue(attendees)
        self.assertEqual(attendees.userid.id, 2)

    def test_cancel_join_trip(self):
        print("----Test: check that users can successfully unjoin a trip")
        c = Client()
        success = c.login(username='hgranger', password='123!@#123')
        response = c.post('/joinTrip/1/') 
        response2 = c.post('/cancelJoin/1/')
        attendees = TripAttendees.objects.all()
        self.assertFalse(attendees)

class Create_Suggestion_View(TestCase):
    def setUpTestData():
        print("Setting up Create_Suggestion_View Tests")
        user1 = User.objects.create_user(username='hpotter', email='hpotter@hogwarts.com', password='123!@#123')
        user2 = User.objects.create_user(username='hgranger', email='hgranger@hogwarts.com', password='123!@#123')
        user1.first_name = "Harry"
        user1.last_name = "Potter"
        user1.save()
        user2.first_name = "Hermione"
        user2.last_name = "Granger"
        user2.save()       
        event1 = Event.objects.create_event("Quittich Pitch", "2021-04-20", 0, user1, 1 )
        TripAttendees.objects.create_attendee(event1, user2)
        pass

    def test_create_suggestion_trip(self):
        print("----Test: check that trip owners can successfully create a suggestion")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        response = c.get('/addSuggestion/1/1/') #go to form page
        #create a suggestion
        response2 = c.post('/addSuggestion/1/1/', {"question_text":"Where are we going the first night?", "end_date_month":2, "end_date_day":3, "end_date_year":2022})
        questions = Question.objects.all()
        self.assertTrue(questions)
        self.assertEqual(questions[0].question_text, "Where are we going the first night?")

    def test_create_suggestion_trip(self):
        print("----Test: check that trip owners can successfully create a choice")
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        #create a suggestion
        response2 = c.post('/addSuggestion/1/1/', {"question_text":"Where are we going the first night?", "end_date_month":2, "end_date_day":3, "end_date_year":2022})
        questions = Question.objects.get(id=1)
        c.post('/addChoice/1/', {"choice_text":"Taco Bell", "cost":23.20})
        c.post('/addChoice/1/', {"choice_text":"McDonalds", "cost":22.50})
        choices = Choice.objects.all()
        self.assertEqual(len(choices), 2)
        self.assertEqual(choices[0].choice_text, "Taco Bell")
        self.assertEqual(str(choices[0].cost), "23.20")
        self.assertEqual(choices[1].choice_text, "McDonalds")
        self.assertEqual(choices[0].question.id, 1)

    def test_vote_on_suggestion(self):
        print("----Test: check that trip attendees can successfully vote on a choice")  
        c = Client()
        success = c.login(username='hpotter', password='123!@#123')
        #create a suggestion
        response2 = c.post('/addSuggestion/1/1/', {"question_text":"Where are we going the first night?", "end_date_month":2, "end_date_day":3, "end_date_year":2022})
        questions = Question.objects.get(id=1)
        c.post('/addChoice/1/', {"choice_text":"Taco Bell", "cost":23.20})
        c.post('/addChoice/1/', {"choice_text":"McDonalds", "cost":22.50})      
        success = c.logout()
        d = Client()
        success = d.login(username='hgranger', password='123!@#123')  
        request = d.get('/displaysuggestion/1/')
        sugg = request.context['question'] 
        qs = request.context['Data']
        self.assertEqual(sugg.question_text, "Where are we going the first night?")
        self.assertEqual(len(qs), 2)
        choice = Choice.objects.get(id=1)
        choice.votes = 2
        choice.save()
        self.assertEqual(choice.votes, 2)
        d.logout()
        c.login(username='hpotter', password='123!@#123')
        c.post('/endvote/1/')
        questions = Question.objects.get(id=1)
        self.assertEqual(questions.resultID, 1)
        





        
