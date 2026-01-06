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
    path('ProfilePage/', userprofile, name='profile'),
    path('Quiz/play/<int:quiz_id>/', play_view, name='play'),
    path('QuizMaker/', quizmaker_view, name='quiz maker'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)