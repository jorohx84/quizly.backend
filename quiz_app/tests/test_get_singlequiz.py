import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question

@pytest.mark.django_db
def test_get_quiz_detail_success():
    """
    Test that GET /api/quizzes/{id}/ returns the specific quiz for the authenticated user
    """
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_authenticate(user=user)

    quiz = Quiz.objects.create(
        user=user,
        title="My Quiz",
        description="Desc",
        video_url="https://youtube.com"
    )
    question = Question.objects.create(
        question_title="What is 2+2?",
        question_options=["1", "2", "3", "4"],
        answer="4"
    )
    quiz.questions.add(question)

    response = client.get(f"/api/quizzes/{quiz.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "My Quiz"
    assert len(data["questions"]) == 1
    assert data["questions"][0]["question_title"] == "What is 2+2?"

@pytest.mark.django_db
def test_get_quiz_detail_forbidden():
    """
    Test that accessing another user's quiz returns 403
    """
    client = APIClient()
    user1 = User.objects.create_user(username="user1", password="12345")
    user2 = User.objects.create_user(username="user2", password="12345")
    client.force_authenticate(user=user1)

    quiz = Quiz.objects.create(user=user2, title="Other Quiz", description="Desc", video_url="https://youtube.com")

    response = client.get(f"/api/quizzes/{quiz.id}/")
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_quiz_detail_not_found():
    """
    Test that accessing a non-existent quiz returns 404
    """
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_authenticate(user=user)

    response = client.get("/api/quizzes/999/")
    assert response.status_code == 404

@pytest.mark.django_db
def test_get_quiz_detail_unauthenticated():
    """
    Test that unauthenticated access returns 401
    """
    client = APIClient()
    response = client.get("/api/quizzes/1/")
    assert response.status_code == 401
