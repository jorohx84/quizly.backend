import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_token_refresh_success():
    """
    Test that a valid refresh token returns a new access token
    """
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="12345")

    login_data = {"username": "testuser", "password": "12345"}
    login_response = client.post("/api/login/", login_data, format="json")

    assert "refresh_token" in login_response.cookies

    response = client.post("/api/token/refresh/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["detail"] == "Token refreshed"
    assert "access" in json_data
    assert "access_token" in response.cookies

@pytest.mark.django_db
def test_token_refresh_unauthorized():
    """
    Test that refresh without a valid token returns 401
    """
    client = APIClient()
    response = client.post("/api/token/refresh/")
    assert response.status_code == 401
