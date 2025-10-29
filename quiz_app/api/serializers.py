from rest_framework import serializers
from ..models import Quiz, Question


    
class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializes a Question object.
    """
    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']




class QuizSerializer(serializers.ModelSerializer):
    """
    Serializes a Quiz object including its related questions.
    """
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'video_url', 'created_at', 'updated_at', 'questions']



class QuizCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a quiz from a YouTube URL.

    Fields:
        - video_url: URL of the YouTube video to generate the quiz from
    """
    url = serializers.URLField()