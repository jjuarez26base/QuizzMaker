from django import forms
from app.models import *

class MakeQuizForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ['title', 'pic', 'owner', 'tags']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].required = False