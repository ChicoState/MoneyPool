
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_slug
from django.core import validators
from django.core.exceptions import ValidationError

from . import models

#validates that email doesn't already exist
def must_be_unique(value):
    user = User.objects.filter(email=value)
    if len(user) > 0:
        raise forms.ValidationError("Email Already in Use")
    return value

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True,
        validators=[must_be_unique]
    )
    first_name = forms.CharField(
        label="first_name",
        required=True
    )
    last_name = forms.CharField(
        label="last_name",
        required=True
    )
    username = forms.CharField(
        label="username",
        required=True
    )
    class Meta:
        model = User
        fields = ("first_name", "last_name","username", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

class EventForm(forms.Form):

    location = forms.CharField(
        label="Where are we going?",
        max_length=30,
        required=True,
    )
    date = forms.DateField(
        label="When are we going?",
        widget=forms.SelectDateWidget(empty_label = ("Choose Year", "Choose Month", "Choose Day"))
    )
    public = forms.BooleanField(
        label="Check this box if trip is open to all friends",
        required=False
    )
    def save(self, request, commit=True):
        trip_instance = models.Event(
            location = self.cleaned_data["location"],
            date = self.cleaned_data["date"],
            attendants = 1,
            invited = 0,
            public = self.cleaned_data["public"],
            author = request.user
        )

        if commit:
            trip_instance.save()
        return trip_instance


class addSuggestion(forms.Form):
    question = forms.CharField(
        label="What is your suggestion?",
        max_length=140,
        required=True,
    )
    def save(self, request, commit=True):
        questionSave = models.Question(
            question = self.cleaned_data["question"],
            author = request.user
        )
        if commit:
            questionSave.save()
        return questionSave
