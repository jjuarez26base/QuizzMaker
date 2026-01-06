from django import forms
from app.models import *

class MakeQuizForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ['title', 'pic', 'owner', 'tags']