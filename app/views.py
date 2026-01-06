
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from . import forms 
from . import models

# Create your views here.
def landing_page_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'LandingPage.html', context)

@login_required(login_url='login')
def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user_profile = models.UserProfile.objects.get(user=request.user)
        context = {"user_profile": user_profile}
    else:
        context = {}
    return render(request, 'home.html', context)

def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            models.UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    context = { 'form': form }
    if request.user.is_authenticated:
        info = models.UserProfile.objects.get(user=request.user)
        context["info"] = info
    return render(request, 'Account/Signup.html', context)

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home') 
        else:
            context = { 'form': form }
            return render(request, "Account/login.html", context)
    else:
        form = AuthenticationForm()
    context = { 'form': form }
    return render(request, 'Account/Login.html', context)

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')

def quiz_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
      user_profile = models.UserProfile.objects.get(user=request.user)
    else:
      user_profile = 'no user profile'
    quizs = models.Quizzes.objects.all()
    context = {"quizs": quizs, "user_profile": user_profile}
    return render(request, "Quizs/all_quizzes.html", context)


#def userprofile(request: HttpRequest) -> HttpResponse:
    #user_to_view = get_object_or_404(User, username=request.user)