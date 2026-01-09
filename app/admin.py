from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Tags)
admin.site.register(models.Quizzes)
admin.site.register(models.Questions)
admin.site.register(models.Choice)
admin.site.register(models.UserQuizAttempt)