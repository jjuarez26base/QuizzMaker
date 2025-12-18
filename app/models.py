from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class Questions(models.Model):
    title= models.CharField(max_length=300)
    pic = models.ImageField(upload_to='images/', blank=True, null=True)
    time = models.IntegerField()
    q1 = models.CharField(max_length=250, default=False)
    q2 = models.CharField(max_length=250, default=False)
    q3 = models.CharField(max_length=250, default=False)
    q4 = models.CharField(max_length=250, default=False) 
    
class Quizzes(models.Model):
    title = models.CharField(max_length=200)
    pic = models.ImageField(upload_to='images/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    questions = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='quizzes')
    tags = models.ManyToManyField(Tags, related_name='quizzes')

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quizzes = models.ForeignKey(Quizzes, on_delete=models.CASCADE, related_name='user_profiles')
    points = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'User: {self.user.username} Quizzes: {self.quizzes.title} Points: {self.points}'