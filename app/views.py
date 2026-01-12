from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, HttpResponse
from . import forms
from . import models
from app.forms import *
from app.models import *
from django.urls import reverse

# Create your views here.
def landing_page_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context = {"user_profile": user_profile}
    else:
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
        form = CreatUser(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('profile')
    else:
        form = CreatUser()
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
    context = {"quizs": quizs, "user_profile": user_profile,}
    return render(request, "Quizs/all_quizzes.html", context)

def search_quiz(request: HttpRequest) -> HttpResponse:
    # searched = "test"
    # print(request.method)
    if request.method == "POST":
        searched = request.POST['search']
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
        else:
            user_profile = 'no user profile'
        if Tags.objects.filter(name = searched).exists():
            tag_on_search = Tags.objects.get(name = searched)
            quizs = Quizzes.objects.filter(tags = tag_on_search.id)
            context = {"quizs": quizs, "user_profile": user_profile, "searched": True, "search_query": searched}
            return render(request, "Quizs/SearchQuizzes.html", context)
    return redirect('quizs')
        


@login_required(login_url='login')
def play_view(request: HttpRequest, quiz_id, question_id) -> HttpResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    quiz = Quizzes.objects.get(id=quiz_id)
    questions = Questions.objects.filter(quiz=quiz).order_by('id')

    find = UserQuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-id')

    if find.exists():
        check_user = find.first()
    else:
        check_user = UserQuizAttempt.objects.create(user=request.user, quiz=quiz)
    total = len(questions)
    outof = total * 10
    if request.method == 'POST':
        if check_user.is_completed:
            context = {"quiz": quiz,
                    "questions": questions,
                    "total": total,
                    'score': check_user.score,
                    'outof': outof,
                    'right_answered':check_user.is_right,
                    'user_profile': user_profile}
            return render(request, "Quizs/play.html", context)
       
        if int(question_id) >= total:
            check_user.is_completed = True
            check_user.save()
            context = {"quiz": quiz,
                       "questions": questions,
                       "total": total,
                       'score': check_user.score,
                       'outof': outof,
                       'right_answered': check_user.is_right,
                       'count': check_user.attempt,
                       'user_profile': user_profile}
            return render(request, "Quizs/play.html", context)
        
        elif int(question_id) < total:
            return redirect('play', quiz_id=quiz.id, question_id=check_user.attempt)
            
        context = {"quiz": quiz,
                    "questions": questions,
                    "total": total, 'score': check_user.score,
                    'outof': outof,
                    'right_answered': check_user.is_right,
                    'user_profile': user_profile}
        return render(request, "Quizs/play.html", context)
    try:
        current = int(question_id)
    except (TypeError, ValueError):
        current = 1

    if total > 0 and current <= total:
        question = list(questions)[current - 1]
        context = {'question': question,
                   'total': total,'current': current,
                   'quiz': quiz, 'user_profile': user_profile}
        return render(request, 'Quizs/play.html', context)
    else:
        score = check_user.score
        right_answered = check_user.is_right
        outof = total * 10
        context = {'question': None,
                   'score': score,
                   'outof': outof,
                   'right_answered': right_answered,
                   'total': total,
                   'count': check_user.attempt,
                   'user_profile': user_profile,
                   'quiz': quiz}
        return render(request, 'Quizs/play.html', context)
    
@login_required(login_url='login')
def play_action(request: HttpRequest, pick) -> HttpResponse:
    ower = request.user
    cho = Quizzes.objects.get(id=pick)
    total = len(cho.questions_set.all())
    check_user = UserQuizAttempt.objects.get(user=ower, quiz=cho)
    check_user.attempt = (int(check_user.attempt) + 1)
    choice_id = request.POST.get('choice_id')
    try:
        choice = Choice.objects.get(id=choice_id)
        if choice.is_correct:
            if int(check_user.score) >= total * 10:
                pass
            else:
                check_user.is_right = (check_user.is_right) + 1
                check_user.score = (check_user.score) + 10
                check_user.save()
                profile = UserProfile.objects.get(user=request.user)
                profile.points = (profile.points) + 10
                profile.save()
    except Choice.DoesNotExist:
        pass
    check_user.save()
    return redirect('play', quiz_id=pick, question_id=check_user.attempt)



def newbio(request):
    if request.method == 'POST':
        owner = UserProfile.objects.get(user=request.user)
        form = ProfileUpdateForm(request.POST, request.FILES, instance=owner)
        if form.is_valid():
            form.save()
    return redirect('profile')
        

def playagain(request: HttpRequest, quiz_id) -> HttpResponse:
    quiz = Quizzes.objects.get(id=quiz_id)
    questions = Questions.objects.filter(quiz=quiz).order_by('id')
    total = len(questions)
    att = UserQuizAttempt.objects.get(user=request.user, quiz=quiz)
    if att.attempt > total:
        att.score = 0
        att.is_right = 0
        att.attempt = 1
        att.is_completed = False
        att.save()
        return redirect('play', quiz_id=quiz_id, question_id=att.attempt)
    return redirect('play', quiz_id=quiz_id, question_id=att.attempt)       
@login_required(login_url='login')
def userprofile(request: HttpRequest) -> HttpResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    user_quizzes = Quizzes.objects.filter(owner=request.user)
    form = ProfileUpdateForm(instance=user_profile)
    context = {
        "user_profile": user_profile,
        "user_quizzes": user_quizzes,
        'form': form
    }
    if request.method == 'POST':
        try:
            delete_quiz = request.POST['delete_quiz']
            quizdel = Quizzes.objects.get(id=delete_quiz)
            quizdel.delete()
            return redirect('profile')
        except:
            pass
    return render(request, 'ProfilePage.html', context)


@login_required(login_url='login')
def quizmaker_view(request: HttpRequest) -> HttpResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    all_tags = Tags.objects.all()
    if request.method == 'GET':
        quiz_form = MakeQuizForm()
        context = {'request': request, "type": 'A get request', 'quiz_form': quiz_form, 'user_profile': user_profile, 'all_tags': all_tags}
    elif request.method == 'POST':
        question_names = []
        question_answers_name = []
        question_answers_content = []
        question_checkboxes_name = []
        counter_list = []
        counter_list_2 = [0]
        question_name_counter = 1
        counter = 0
        for item in request.POST.items():
            question_answers_list = [f'question_{counter}answer1', f'question_{counter}answer2', 
                                    f'question_{counter}answer3', f'question_{counter}answer4']
            question_checkboxes_list = [f'question_{counter}answer1checkbox', f'question_{counter}answer2checkbox',
                                        f'question_{counter}answer3checkbox', f'question_{counter}answer4checkbox']
            if item[0] == f'question_{question_name_counter}':
                question_names.append(item)
                question_name_counter += 1
                counter += 1
                counter_list.append(counter)
                counter_list_2.append(counter)
            elif item[0] in question_answers_list:
                question_answers_name.append(item[0])
                question_answers_content.append(item[1])
            elif item[0] in question_checkboxes_list:
                question_checkboxes_name.append(item[0])
        question_list = []
        for question_info in question_names:
            question_set = [] 
            question_number = question_info[0]
            question_title = question_info[1]
            question_set.append(question_number)
            question_set.append(question_title)
            try:
                answer_1_index = question_answers_name.index(f"{question_number}answer1")
                question_set.append(question_answers_name[answer_1_index])
                question_set.append(question_answers_content[answer_1_index])
            except:
                answer_1_index = 'no answer 1'
                answer_1_value = 'none'
                question_set.append(answer_1_index)
                question_set.append(answer_1_value)
            try:
                checkbox_1_index = question_checkboxes_name.index(f"{question_number}answer1checkbox")
                question_set.append(question_checkboxes_name[checkbox_1_index])
            except:
                checkbox_1_index = 'wrong'
                question_set.append(checkbox_1_index)
            try:
                answer_2_index = question_answers_name.index(f"{question_number}answer2")
                question_set.append(question_answers_name[answer_2_index])
                question_set.append(question_answers_content[answer_2_index])
            except:
                answer_2_index = 'no answer 2'
                answer_2_value = 'none'
                question_set.append(answer_2_index)
                question_set.append(answer_2_value)
            try:
                checkbox_2_index = question_checkboxes_name.index(f"{question_number}answer2checkbox")
                question_set.append(question_checkboxes_name[checkbox_2_index])
            except:
                checkbox_2_index = 'wrong'
                question_set.append(checkbox_2_index)
            try:
                answer_3_index = question_answers_name.index(f"{question_number}answer3")
                question_set.append(question_answers_name[answer_3_index])
                question_set.append(question_answers_content[answer_3_index])
            except:
                answer_3_index = 'no answer 3'
                answer_3_value = 'none'
                question_set.append(answer_3_index)
                question_set.append(answer_3_value)
            try:
                checkbox_3_index = question_checkboxes_name.index(f"{question_number}answer3checkbox")
                question_set.append(question_checkboxes_name[checkbox_3_index])
            except:
                checkbox_3_index = 'wrong'
                question_set.append(checkbox_3_index)
            try:
                answer_4_index = question_answers_name.index(f"{question_number}answer4")
                question_set.append(question_answers_name[answer_4_index])
                question_set.append(question_answers_content[answer_4_index])
            except:
                answer_4_index = 'no answer 4'
                answer_4_value = 'none'
                question_set.append(answer_4_index)
                question_set.append(answer_4_value)
            try:
                checkbox_4_index = question_checkboxes_name.index(f"{question_number}answer4checkbox")
                question_set.append(question_checkboxes_name[checkbox_4_index])
            except:
                checkbox_4_index = 'wrong'
                question_set.append(checkbox_4_index)
            question_list.append(question_set)
        quiz_form = MakeQuizForm(request.POST, request.FILES)
        forms_good = True
        if quiz_form.is_valid():
            quiz_instance = quiz_form.save(commit=False)
            quiz_instance.owner = request.user
            quiz_instance.save()
            quiz_form.save_m2m()
            quiz = quiz_instance
        else:
            forms_good = False
        question_form_list = []
        if forms_good != False:
            for question in question_list:
                question_form = MakeQuestionForm({'quiz': quiz, 'question': question[1]})
                if question_form.is_valid():
                    current_question = question_form.save()
                    if question[3] != 'none':
                        if question[4] != 'wrong':
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[3], 'is_correct': True})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                        else:
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[3], 'is_correct': False})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                    if question[6] != 'none':
                        if question[7] != 'wrong':
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[6], 'is_correct': True})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                        else:
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[6], 'is_correct': False})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                    if question[9] != 'none':
                        if question[10] != 'wrong':
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[9], 'is_correct': True})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                        else:
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[9], 'is_correct': False})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                    if question[12] != 'none':
                        if question[13] != 'wrong':
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[12], 'is_correct': True})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                        else:
                            choice_form = MakeChoiceForm({'question': current_question, 'text': question[12], 'is_correct': False})
                            if choice_form.is_valid():
                                choice_form.save()
                            else:
                                forms_good = False
                else:
                    forms_good = False
                question_form_list.append(question_form)
            return redirect('profile')
        
        context = {'request': question_form_list, "type": 'Quiz was made', 'quiz_form': quiz_form, 'user_profile': user_profile, 'all_tags': all_tags}
        if forms_good == False:
            question_names = []
            question_answers_name = []
            question_answers_content = []
            question_checkboxes_name = []
            counter_list = []
            counter_list_2 = [0]
            question_name_counter = 1
            counter = 0
            for item in request.POST.items():
                question_answers_list = [f'question_{counter}answer1', f'question_{counter}answer2', 
                                        f'question_{counter}answer3', f'question_{counter}answer4']
                question_checkboxes_list = [f'question_{counter}answer1checkbox', f'question_{counter}answer2checkbox',
                                            f'question_{counter}answer3checkbox', f'question_{counter}answer4checkbox']
                if item[0] == f'question_{question_name_counter}':
                    question_names.append(item)
                    question_name_counter += 1
                    counter += 1
                    counter_list.append(counter)
                    counter_list_2.append(counter)
                elif item[0] in question_answers_list:
                    question_answers_name.append(item[0])
                    question_answers_content.append(item[1])
                elif item[0] in question_checkboxes_list:
                    question_checkboxes_name.append(item[0])
            question_list = []
            question_counter = 1
            for question_info in question_names:
                question_set = []
                question_set.append(question_counter)
                question_counter += 1
                question_number = question_info[0]
                question_title = question_info[1]
                question_set.append(question_number)
                question_set.append(question_title)
                try:
                    answer_1_index = question_answers_name.index(f"{question_number}answer1")
                    question_set.append(question_answers_name[answer_1_index])
                    question_set.append(question_answers_content[answer_1_index])
                except:
                    answer_1_index = 'none'
                    question_set.append(answer_1_index)
                try:
                    checkbox_1_index = question_checkboxes_name.index(f"{question_number}answer1checkbox")
                    question_set.append(question_checkboxes_name[checkbox_1_index])
                except:
                    checkbox_1_index = 'wrong'
                    question_set.append(checkbox_1_index)
                try:
                    answer_2_index = question_answers_name.index(f"{question_number}answer2")
                    question_set.append(question_answers_name[answer_2_index])
                    question_set.append(question_answers_content[answer_2_index])
                except:
                    answer_2_index = 'none'
                    question_set.append(answer_2_index)
                try:
                    checkbox_2_index = question_checkboxes_name.index(f"{question_number}answer2checkbox")
                    question_set.append(question_checkboxes_name[checkbox_2_index])
                except:
                    checkbox_2_index = 'wrong'
                    question_set.append(checkbox_2_index)
                try:
                    answer_3_index = question_answers_name.index(f"{question_number}answer3")
                    question_set.append(question_answers_name[answer_3_index])
                    question_set.append(question_answers_content[answer_3_index])
                except:
                    answer_3_index = 'none'
                    question_set.append(answer_3_index)
                try:
                    checkbox_3_index = question_checkboxes_name.index(f"{question_number}answer3checkbox")
                    question_set.append(question_checkboxes_name[checkbox_3_index])
                except:
                    checkbox_3_index = 'wrong'
                    question_set.append(checkbox_3_index)
                try:
                    answer_4_index = question_answers_name.index(f"{question_number}answer4")
                    question_set.append(question_answers_name[answer_4_index])
                    question_set.append(question_answers_content[answer_4_index])
                except:
                    answer_4_index = 'none'
                    question_set.append(answer_4_index)
                try:
                    checkbox_4_index = question_checkboxes_name.index(f"{question_number}answer4checkbox")
                    question_set.append(question_checkboxes_name[checkbox_4_index])
                except:
                    checkbox_4_index = 'wrong'
                    question_set.append(checkbox_4_index)
                question_list.append(question_set)
            context = {'request': question_list, "type": 'Failed to make Quiz', 'quiz_form': quiz_form, 'user_profile': user_profile, 'all_tags': all_tags}
            return render(request, "Quizs/quiz_maker.html", context)
    else:
        context = {'request': 'none', "type": 'No request', 'user_profile': user_profile, 'all_tags': all_tags}
    return render(request, "Quizs/quiz_maker.html", context)

@login_required(login_url='login')
def quizeditor_view(request: HttpRequest) -> HttpResponse:
    user_profile = UserProfile.objects.get(user=request.user)
    user_quizzes = Quizzes.objects.filter(owner=request.user)
    all_tags = Tags.objects.all()
    if request.method == 'GET':
        quiz = 'none'
        quiz_form = 'none'
        
        context = {'specific_quiz': quiz, "user_profile": user_profile, "quizs": user_quizzes, 'quiz_form': quiz_form, 'all_tags': all_tags}
        return render(request, 'Quizs/edit_quiz.html', context)

    elif request.method == 'POST':
        print(request.POST)
        try:
            specific_quiz_pk = request.POST['pk']
        except:
            delete_quiz = request.POST['delete_quiz']
            quizdel = Quizzes.objects.get(id=delete_quiz)
            quizdel.delete()
            return redirect('quiz editor')
        specific_quiz = Quizzes.objects.get(pk=specific_quiz_pk)
        try:
            specific_quiz = Quizzes.objects.get(pk=specific_quiz_pk)
            if specific_quiz.owner == request.user:
                quiz = specific_quiz
                questions = Questions.objects.filter(quiz=quiz)
            else:
                quiz = 'none'
        except:
            quiz = 'none'
        update_quiz = False
        if quiz != 'none' and request.POST.get('question_1') != None:
            update_quiz = True
        else:
            update_quiz = False

        if quiz != 'none' and update_quiz == False:
            quiz_form = MakeQuizForm(initial={'title': quiz.title, 'pic': quiz.pic, 'owner': quiz.owner, 'tags': quiz.tags.all()})
            question_list = []
            counter = 1

            for question_object in questions:
                question_id = f'question_{counter}'                
                question_id_answer_list = [f'question_{counter}', f'question_{counter}', 
                                        f'question_{counter}', f'question_{counter}']
                question_set = []
                question_set.append(counter)
                counter += 1
                question_set.append(MakeQuestionForm(initial={'question': question_object.question}))
                try:
                    choices = Choice.objects.filter(question=question_object)
                    for choice in choices:
                        question_set.append(MakeChoiceForm(initial={'text': choice.text, 'is_correct': choice.is_correct}))
                except:
                    pass
                question_set.append(question_id)
                question_set.append(question_id_answer_list)
                question_set.append(question_object.pk)
                question_list.append(question_set)
            context = {'question_list': question_list, 'specific_quiz': quiz, "user_profile": user_profile, 
                    "quizs": user_quizzes, 'quiz_form': quiz_form, 'questions': questions, 'pk': specific_quiz_pk, 'all_tags': all_tags}
            
        elif quiz != 'none' and update_quiz == True:
            question_names = []
            question_answers_name = []
            question_answers_content = []
            question_checkboxes_name = []
            counter_list = []
            counter_list_2 = [0]
            question_name_counter = 1
            counter = 0
            for item in request.POST.items():
                question_answers_list = [f'question_{counter}answer1', f'question_{counter}answer2', 
                                        f'question_{counter}answer3', f'question_{counter}answer4']
                question_checkboxes_list = [f'question_{counter}answer1checkbox', f'question_{counter}answer2checkbox',
                                            f'question_{counter}answer3checkbox', f'question_{counter}answer4checkbox']
                if item[0] == f'question_{question_name_counter}':
                    question_names.append(item)
                    question_name_counter += 1
                    counter += 1
                    counter_list.append(counter)
                    counter_list_2.append(counter)
                elif item[0] in question_answers_list:
                    question_answers_name.append(item[0])
                    question_answers_content.append(item[1])
                elif item[0] in question_checkboxes_list:
                    question_checkboxes_name.append(item[0])
            question_list = []
            for question_info in question_names:
                question_set = [] 
                question_number = question_info[0]
                question_title = question_info[1]
                question_set.append(question_number)
                question_set.append(question_title)
                try:
                    answer_1_index = question_answers_name.index(f"{question_number}answer1")
                    question_set.append(question_answers_name[answer_1_index])
                    question_set.append(question_answers_content[answer_1_index])
                except:
                    answer_1_index = 'no answer 1'
                    answer_1_value = 'none'
                    question_set.append(answer_1_index)
                    question_set.append(answer_1_value)
                try:
                    checkbox_1_index = question_checkboxes_name.index(f"{question_number}answer1checkbox")
                    question_set.append(question_checkboxes_name[checkbox_1_index])
                except:
                    checkbox_1_index = 'wrong'
                    question_set.append(checkbox_1_index)
                try:
                    answer_2_index = question_answers_name.index(f"{question_number}answer2")
                    question_set.append(question_answers_name[answer_2_index])
                    question_set.append(question_answers_content[answer_2_index])
                except:
                    answer_2_index = 'no answer 2'
                    answer_2_value = 'none'
                    question_set.append(answer_2_index)
                    question_set.append(answer_2_value)
                try:
                    checkbox_2_index = question_checkboxes_name.index(f"{question_number}answer2checkbox")
                    question_set.append(question_checkboxes_name[checkbox_2_index])
                except:
                    checkbox_2_index = 'wrong'
                    question_set.append(checkbox_2_index)
                try:
                    answer_3_index = question_answers_name.index(f"{question_number}answer3")
                    question_set.append(question_answers_name[answer_3_index])
                    question_set.append(question_answers_content[answer_3_index])
                except:
                    answer_3_index = 'no answer 3'
                    answer_3_value = 'none'
                    question_set.append(answer_3_index)
                    question_set.append(answer_3_value)
                try:
                    checkbox_3_index = question_checkboxes_name.index(f"{question_number}answer3checkbox")
                    question_set.append(question_checkboxes_name[checkbox_3_index])
                except:
                    checkbox_3_index = 'wrong'
                    question_set.append(checkbox_3_index)
                try:
                    answer_4_index = question_answers_name.index(f"{question_number}answer4")
                    question_set.append(question_answers_name[answer_4_index])
                    question_set.append(question_answers_content[answer_4_index])
                except:
                    answer_4_index = 'no answer 4'
                    answer_4_value = 'none'
                    question_set.append(answer_4_index)
                    question_set.append(answer_4_value)
                try:
                    checkbox_4_index = question_checkboxes_name.index(f"{question_number}answer4checkbox")
                    question_set.append(question_checkboxes_name[checkbox_4_index])
                except:
                    checkbox_4_index = 'wrong'
                    question_set.append(checkbox_4_index)
                question_list.append(question_set)

            new_quiz_form = EditQuizForm(request.POST, request.FILES, instance=quiz)
            print()
            print(new_quiz_form)
            print()
            if new_quiz_form.is_valid():
                quiz = new_quiz_form.save()
                print('saved quiz')
            else:
                print('did not save quiz')
                pass

            counter_list_2.pop()
            for number in counter_list_2:
                question_form = EditQuestionForm({'question': question_list[number][1]}, instance=questions[number])
                if question_form.is_valid():
                    question_form.save()
                choices = Choice.objects.filter(question=questions[number])
                answer_counter = 3
                correct_counter = 4
                for choice in choices:
                    if question_list[number][correct_counter] == 'wrong':
                        choice_form = EditChoiceForm({'text': question_list[number][answer_counter], 'is_correct': False}, instance=choice)
                    else:
                        choice_form = EditChoiceForm({'text': question_list[number][answer_counter], 'is_correct': True}, instance=choice)
                    if choice_form.is_valid():
                        choice_form.save()
                        answer_counter += 3
                        correct_counter += 3
            return redirect('profile')

        else:
            context = {'specific_quiz': quiz, "user_profile": user_profile, 'all_tags': all_tags}
    return render(request, 'Quizs/edit_quiz.html', context)

@staff_member_required
def admin_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_to_toggle = get_object_or_404(User, id=request.POST['chips'])
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        return redirect('admin')
    user_profile = UserProfile.objects.get(user=request.user)
    total_users = UserProfile.objects.count()
    total_quizzes = Quizzes.objects.count()
    recent_quizzes = Quizzes.objects.order_by('-created_at')[:5]
    all_users = User.objects.all()

    context = {
        "total_users": total_users,
        "total_quizzes": total_quizzes,
        "recent_quizzes": recent_quizzes,
        "all_users": all_users,'user_profile': user_profile
    }
    return render(request, 'AdminPage.html', context)

@staff_member_required
def admin_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user_to_toggle = get_object_or_404(User, id=request.POST['chips'])
        user_to_toggle.is_active = not user_to_toggle.is_active
        user_to_toggle.save()
        return redirect('admin')
    user_profile = UserProfile.objects.get(user=request.user)
    total_users = UserProfile.objects.count()
    total_quizzes = Quizzes.objects.count()
    recent_quizzes = Quizzes.objects.order_by('-created_at')[:5]
    all_users = User.objects.all()

    context = {
        "total_users": total_users,
        "total_quizzes": total_quizzes,
        "recent_quizzes": recent_quizzes,
        "all_users": all_users,'user_profile': user_profile
    }
    return render(request, 'AdminPage.html', context)

def delete4admin(request, quiz_id):
    quizdel = Quizzes.objects.get(id=quiz_id)
    quizdel.delete()
    return redirect('admin')

def delete4user(request, quiz_id):
    quizdel = Quizzes.objects.get(id=quiz_id)
    quizdel.delete()
    return redirect('quizs')

def delete_question_view(request: HttpRequest, question_id: int) -> HttpResponse:
    delete_question = Questions.objects.get(id=question_id)
    delete_question.delete()
    return redirect('quiz editor')