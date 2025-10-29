import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_login_success():
    """
    Test that a user can login successfully with correct credentials
    """
    user = User.objects.create_user(username="testuser", password="12345", email="test@example.com")
    client = APIClient()

    data = {
        "username": "testuser",
        "password": "12345"
    }

    response = client.post("/api/login/", data, format="json")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["detail"] == "Login successfully!"
    assert json_data["user"]["username"] == "testuser"
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies

@pytest.mark.django_db
def test_login_invalid_credentials():
    """
    Test login fails with wrong username or password
    """
    User.objects.create_user(username="testuser", password="12345")
    client = APIClient()

    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    response = client.post("/api/login/", data, format="json")
    assert response.status_code == 401

@pytest.mark.django_db
def test_login_missing_fields():
    """
    Test login fails if required fields are missing
    """
    client = APIClient()
    data = {
        "username": "testuser"
    }

    response = client.post("/api/login/", data, format="json")
    assert response.status_code == 400
