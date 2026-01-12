from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import *

class CreatUser(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 10
        self.fields['username'].widget.attrs['maxlength'] = 10

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['pic', 'bio'] 

class MakeQuizForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ['title', 'pic', 'owner', 'tags']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].required = False

class MakeQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['quiz', 'question']

class MakeChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text', 'is_correct']

class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question']

class EditChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

class EditQuizForm(forms.ModelForm):
    class Meta:
        model = Quizzes
        fields = ['title', 'pic', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = False