import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_logout_success():
    """
    Test that a logged-in user can logout successfully
    """
    client = APIClient()
    user = User.objects.create_user(username="testuser", password="12345")

    # Login, um Tokens zu setzen
    login_data = {"username": "testuser", "password": "12345"}
    login_response = client.post("/api/login/", login_data, format="json")
    assert login_response.status_code == 200

    # Logout request
    response = client.post("/api/logout/")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["detail"].startswith("Log-Out successfully")

    # Prüfen, dass Cookies gelöscht wurden
    assert "access_token" not in response.cookies or response.cookies["access_token"].value == ""
    assert "refresh_token" not in response.cookies or response.cookies["refresh_token"].value == ""

@pytest.mark.django_db
def test_logout_unauthenticated():
    """
    Test that logout without authentication returns 401
    """
    client = APIClient()
    response = client.post("/api/logout/")
    assert response.status_code == 401
