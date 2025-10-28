import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question

@pytest.mark.django_db
def test_get_quizzes_returns_user_quizzes():
    """
    Test that GET /api/quizzes/ returns quizzes for the authenticated user
    """
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_authenticate(user=user)

    # Test-Quiz erstellen
    quiz = Quiz.objects.create(
        user=user,
        title="Test Quiz",
        description="Desc",
        video_url="https://youtube.com"
    )

    # Frage erstellen
    question = Question.objects.create(
        question_title="Was ist 2+2?",
        question_options=["1", "2", "3", "4"],
        answer="4"
    )

    # Frage zum Quiz hinzufügen
    quiz.questions.add(question)

    # API Request
    response = client.get("/api/quizzes/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Quiz"  # stimmt jetzt mit erstellt
    assert len(data[0]["questions"]) == 1
    assert data[0]["questions"][0]["question_title"] == "Was ist 2+2?"  # deutsch

