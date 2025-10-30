from django.contrib import admin
from .models import Quiz, Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0  

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')
    inlines = [QuestionInline]  


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'quiz', 'created_at')