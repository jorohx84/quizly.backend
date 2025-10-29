import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question

@pytest.mark.django_db
def test_patch_quiz_partial_update():
    """
    Test partial update of a quiz via PATCH /api/quizzes/{id}/
    """
    client = APIClient()

    user1 = User.objects.create_user(username="user1", password="12345")
    user2 = User.objects.create_user(username="user2", password="12345")

 
    quiz = Quiz.objects.create(
        user=user1,
        title="Original Title",
        description="Original Description",
        video_url="https://youtube.com"
    )

   
    question = Question.objects.create(
        question_title="Was ist 2+2?",
        question_options=["1", "2", "3", "4"],
        answer="4"
    )
    quiz.questions.add(question)

   
    client.force_authenticate(user=user1)
    response = client.patch(f"/api/quizzes/{quiz.id}/", {"title": "Updated Title"}, format="json")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original Description"

  
    client.force_authenticate(user=user2)
    response = client.patch(f"/api/quizzes/{quiz.id}/", {"title": "Hacked Title"}, format="json")
    assert response.status_code in [403, 404]  
    quiz.refresh_from_db()
    assert quiz.title == "Updated Title" 

  
    client.force_authenticate(user=None)
    response = client.patch(f"/api/quizzes/{quiz.id}/", {"title": "Anonymous Update"}, format="json")
    assert response.status_code == 401
