from django.db import models
from django.contrib.auth.models import User
class Question(models.Model):
    question_title = models.CharField(max_length=255)
    question_options = models.JSONField()
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes") 
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_url = models.CharField(max_length=255)
    questions = models.ManyToManyField(Question, related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


