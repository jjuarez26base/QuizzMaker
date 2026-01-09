from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', landing_page_view, name='landing page'),
    path('home', home, name='home'),
    path('Signup/', signup_view, name='signup'),
    path('Login/', login_view, name='login'),
    path('Logout/', logout_view, name='logout'),
    path('Quizs', quiz_list, name='quizs'),
    path('Quizs/Search/', search_quiz, name='search'),
    path('delete/<int:quiz_id>/', delete4user , name='delete quiz'),
    path('ProfilePage/', userprofile, name='profile'),
    path('update/', newbio, name='newbio'),
    path('AdminPage/', admin_view, name='admin'),
    path('adimindelete/<int:quiz_id>/', delete4admin , name='admin delete'),
    path('Quiz/play/<int:quiz_id>/<int:question_id>/', play_view, name='play'),
    path('Action/<int:pick>/', play_action, name='playchoice'),
    path('start/<int:quiz_id>/', playagain, name='startover'),
    path('QuizMaker/', quizmaker_view, name='quiz maker'),
    path('EditQuiz/', quizeditor_view, name='quiz editor'),
    path('delete_question/<int:question_id>/', delete_question_view, name='delete question'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)