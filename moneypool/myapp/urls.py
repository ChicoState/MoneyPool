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
    path('viewtrips/', views.viewTrips_view)
]