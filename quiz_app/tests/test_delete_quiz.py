import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question

@pytest.mark.django_db

def test_delete_quiz():
    """
    Test deleting a quiz via DELETE /api/quizzes/{id}/
    """
    client = APIClient()

    user1 = User.objects.create_user(username="user1", password="12345")
    user2 = User.objects.create_user(username="user2", password="12345")

    quiz = Quiz.objects.create(
        user=user1,
        title="Test Quiz",
        description="Desc",
        video_url="https://youtube.com"
    )

    question = Question.objects.create(
        question_title="Was ist 2+2?",
        question_options=["1", "2", "3", "4"],
        answer="4"
    )
    quiz.questions.add(question)

   
    client.force_authenticate(user=user1)
    response = client.delete(f"/api/quizzes/{quiz.id}/")
    assert response.status_code == 204
    assert not Quiz.objects.filter(id=quiz.id).exists()
    assert Question.objects.filter(id=question.id).exists()

  
    quiz2 = Quiz.objects.create(
        user=user1,
        title="Another Quiz",
        description="Desc",
        video_url="https://youtube.com"
    )
    client.force_authenticate(user=user2)
    response = client.delete(f"/api/quizzes/{quiz2.id}/")
    assert response.status_code == 403 
    assert Quiz.objects.filter(id=quiz2.id).exists()
