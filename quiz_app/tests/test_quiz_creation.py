import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from quiz_app.models import Quiz

@pytest.mark.django_db
def test_create_quiz_view_creates_quiz(monkeypatch):
    """
    Test that POST /api/createQuiz/ successfully creates a Quiz object.
    """
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="12345")
    client.force_authenticate(user=user)

    # ✅ Fake Gemini + Audio-Download pipeline
    monkeypatch.setattr("quiz_app.api.functions.download_audio", lambda url: "fake_audio.mp3")
    monkeypatch.setattr("quiz_app.api.functions.transcribe_audio", lambda f: "Fake transcript")
    monkeypatch.setattr(
        "quiz_app.api.functions.generate_quiz",
        lambda t: ({
            "title": "Test Quiz",
            "description": "A generated quiz",
            "questions": [
                {
                    "question_title": "Was ist 2+2?",
                    "question_options": ["1", "2", "3", "4"],
                    "answer": "4"
                }
            ]
        }, "RAW")
    )

    response = client.post("/api/createQuiz/", {"video_url": "https://youtube.com/watch?v=test"}, format="json")

    # ✅ Expect HTTP 201 CREATED
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Quiz"
    assert Quiz.objects.count() == 1
