from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from . import forms
from . import models
from app.forms import *
from app.models import *
from django.urls import reverse

# Create your views here.
def landing_page_view(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, 'LandingPage.html', context)

@login_required(login_url='login')
def home(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"user_profile": user_profile}
    else:
        context = {}
    return render(request, 'home.html', context)

def signup_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home') 
    else:
        form = UserCreationForm()
    context = { 'form': form }
    if request.user.is_authenticated:
        info = UserProfile.objects.get(user=request.user)
        context["info"] = info
    return render(request, 'Account/Signup.html', context)

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
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
      user_profile = UserProfile.objects.get(user=request.user)
    else:
      user_profile = 'no user profile'
    quizs = Quizzes.objects.all()
    context = {"quizs": quizs, "user_profile": user_profile}
    return render(request, "Quizs/all_quizzes.html", context)

def play_view(request: HttpRequest, quiz_id, question_id) -> HttpResponse:
    quiz = Quizzes.objects.get(id=quiz_id)
    questions = Questions.objects.filter(quiz=quiz).order_by('-id')
    total = len(questions)
    key = f'quiz_{quiz_id}'
    progress = request.session.get(key)
    choice_id = request.POST.get('choice_id')
    outof = total * 10
    q = int(question_id)

    if request.method == 'POST':
        if progress is None:
            progress = {'questions_answered': 0, 'score': 0, "right_answered": 0}
        try:
            choice = Choice.objects.get(id=choice_id)
            if choice.is_correct:
                progress['score'] = progress.get('score') + 10
                progress['right_answered'] = progress.get('right_answered') + 1
        except Choice.DoesNotExist:
            pass
        progress['questions_answered'] = progress.get('questions_answered') + 1
        request.session[key] = progress

        if int(question_id) >= total:
            score = progress.get('score')
            right_answered = progress.get('right_answered')
            try:
                del request.session[key]
            except KeyError:
                pass

            context = {"quiz": quiz, "questions": questions, "total": total, "outof": outof, "score": score, "right_answered": right_answered}
            return render(request, "Quizs/play.html", context)
        
            
       
    else:
        context = {"quiz": quiz, "questions": questions, "question_id": question_id, "total": total, "outof": outof, "progress": progress, "question": q}
        return render(request, "Quizs/play.html", context)
       
            
       
@login_required(login_url='login')
def userprofile(request: HttpRequest) -> HttpResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    user_quizzes = Quizzes.objects.filter(owner=request.user)
    context = {
        "user_profile": user_profile,
        "user_quizzes": user_quizzes
    }
    return render(request, 'ProfilePage.html', context)

@login_required(login_url='login')
def quizmaker_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        form = MakeQuizForm()
        context = {'request': request, "type": 'A get request', 'form': form}
    elif request.method == 'POST':
        form = MakeQuizForm(request.POST, request.FILES)
        if form.is_valid() == False:
            # quiz_instance = form.save(commit=False)
            # quiz_instance.owner = request.user
            # quiz_instance.save()
            # form.save_m2m()
            context = {'request': request.POST, "type": 'Quiz was made', 'form': form}
        else:
            question_names = []
            question_answers = []
            question_answers_checkboxes = []
            question_name_counter = 1
            question_answers_counter = 0
            question_checkboxes_counter = 0
            for item in request.POST.items():
                question_answers_list = [f'question_{question_answers_counter}answer1', 
                                         f'question_{question_answers_counter}answer2', 
                                         f'question_{question_answers_counter}answer3', 
                                         f'question_{question_answers_counter}answer4']
                question_answers_checkboxes_list = [f'question_{question_checkboxes_counter}answer1checkbox',
                                                    f'question_{question_checkboxes_counter}answer2checkbox',
                                                    f'question_{question_checkboxes_counter}answer3checkbox',
                                                    f'question_{question_checkboxes_counter}answer4checkbox']
                if item[0] == f'question_{question_name_counter}':
                    question_names.append(item)
                    question_name_counter += 1
                    question_answers_counter += 1
                    question_answers_checkboxs_counter += 1
                elif item[0] in question_answers_list:
                    question_answers.append(item)
            context = {'request': request.POST, "type": 'Failed to make Quiz', 'form': form}
            return render(request, "Quizs/quiz_maker.html", context)
    else:
        context = {'request': 'none', "type": 'No request'}
    return render(request, "Quizs/quiz_maker.html", context)