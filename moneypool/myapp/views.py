from django.shortcuts import render, redirect
from . import models, forms
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from . import forms

# Create your views here.


#Login View
@login_required(login_url='/login/')
def index(request):
        if request.user.is_authenticated:
            u = User.objects.get(username=request.user.username)
            context = {
                "title":"My Profile",
                "page_name":"Moneypool",
                "name": u.first_name,
                "data": u
            }
            return render(request, "profile.html", context=context)
        else:
            return redirect('/login/')



#logout
def logout_view(request):
    logout(request)
    return redirect("/login/")

#registration view
def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

