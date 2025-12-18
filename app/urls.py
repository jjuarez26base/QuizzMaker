from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('Signup/', signup_view, name='signup'),
    path('Login/', login_view, name='login'),
    path('Logout/', logout_view, name='logout'),
    path('Quizs', quiz_list, name='quizs')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)