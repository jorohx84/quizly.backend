from rest_framework import serializers
from ..models import Quiz, Question

class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'createa_at', 'updated_at']
    
    def get_question_options(self, obj):
        return obj.question_options.split(';')
    


class QuizCreateSerializer(serializers.Serializer):
    video_url = serializers.URLField()