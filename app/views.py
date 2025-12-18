
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import forms 
from . import models

# Create your views here.


# @login_required(login_url='signup')
def home(request):
    context = {}
    return render(request, 'home.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    context = { 'form': form }
    return render(request, 'Account/Signup.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home') 
    else:
        form = AuthenticationForm()
    context = { 'form': form }
    return render(request, 'Account/Login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def quiz_list(requst):
    quizs = models.Quizzes.objects.all()
    context = {"quizs": quizs}
    return render(requst, "Quizs/all_quizzes.html", context)