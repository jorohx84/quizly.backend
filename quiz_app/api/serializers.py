from rest_framework import serializers
from ..models import Quiz, Question

# class QuestionSerializer(serializers.ModelSerializer):
#     question_options = serializers.SerializerMethodField()

#     class Meta:
#         model = Question
#         fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']
    
#     def get_question_options(self, obj):
#         return obj.question_options.split(';')
    
class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']

    def get_question_options(self, obj):
        # Trennt nach Komma und entfernt leere Strings
        return [opt.strip() for opt in obj.question_options.split(',') if opt.strip()]


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'video_url', 'created_at', 'updated_at', 'questions']

class QuizCreateSerializer(serializers.Serializer):
    video_url = serializers.URLField()