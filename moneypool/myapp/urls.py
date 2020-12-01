from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

app_name = 'suggestions'

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
    path('register/', views.register),
    path('index/', views.index),
    path('addtrip/', views.addTrip_form_view),
    path('endvote/<int:question_id>/', views.endvote),
    path('viewtrips/', views.viewTrips_view),
    path('profile/', views.index),
    path('findUsers/', views.findUsers),
    path('profile/<int:id>', views.profile2),
    path('sendRequest/<int:id>', views.sendFR),
    path('tripdetails/<int:tripID>/', views.tripDetails_view),
    path('sendRequest/<int:id>', views.sendFR),
    path('acceptTripReq/<int:id>/', views.acceptTripReq),
    path('joinTrip/<int:id>/', views.joinTrip),
    path('cancelJoin/<int:id>/', views.cancelJoin),
    path('populateTables/', views.populateTrips),
    path('populateUsers/', views.populateUsers),
    path('suggestions/', views.suggestionIndex, name ='suggestionsIndex'),
    path('displaysuggestion/<int:question_id>/', views.displaySuggestion),
    path('addSuggestion/<str:category>/<int:trip_id>/', views.addSuggestion),
    path('addChoice/<int:sugg_id>/', views.addChoice, name='addChoice'),    
    path('suggestions/<int:question_id>/', views.suggestionDetail, name = 'details'),
    path('suggestions/<int:question_id>/results', views.suggestionResults, name = 'results'),
    path('suggestions/<int:question_id>/vote', views.suggestionVote, name = 'vote'),
    path('tripdetails/<int:tripID>/categoryPage/<int:category_ID>/', views.categoryPageView),
    ]
