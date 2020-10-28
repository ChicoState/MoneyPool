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
    path('viewtrips/', views.viewTrips_view),
    path('profile/', views.index),
    path('suggestions/', views.suggestionIndex, name ='suggestionsIndex'),
    path('suggestions/<int:question_id>/', views.suggestionDetail, name = 'details'),
    path('suggestions/<int:question_id>/results', views.suggestionResults, name = 'results'),
    path('suggestions/<int:question_id>/vote', views.suggestionVote, name = 'vote'),
]
