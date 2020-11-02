from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.index),
    path('login/', auth_views.LoginView.as_view()),
    path('logout/', views.logout_view),
    path('register/', views.register),
    path('index/', views.index),
    path('addtrip/', views.addTrip_form_view),
    path('viewtrips/', views.viewTrips_view),
    path('profile/', views.index),
    path('findUsers/', views.findUsers),
    path('profile/<int:id>', views.profile2),
    path('sendRequest/<int:id>', views.sendFR)
    path('tripdetails/<int:tripID>/', views.tripDetails_view)
    path('sendRequest/<int:id>', views.sendFR),
    path('populateTables/', views.populateTrips),
    path('populateUsers/', views.populateUsers)
]