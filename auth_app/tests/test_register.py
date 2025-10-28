import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_register_success():
    """
    Test successful user registration
    """
    client = APIClient()
    data = {
        "username": "newuser",
        "password": "securepassword123",
        "confirmed_password": "securepassword123",
        "email": "newuser@example.com"
    }
    response = client.post("/api/register/", data, format="json")
    assert response.status_code == 201
    assert response.json()["detail"] == "User created successfully!"
    assert User.objects.filter(username="newuser").exists()

@pytest.mark.django_db
def test_register_missing_fields():
    """
    Test registration fails if required fields are missing
    """
    client = APIClient()
    data = {
        "username": "user2",
        # password fehlt
        "confirmed_password": "something",
        "email": "user2@example.com"
    }
    response = client.post("/api/register/", data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_register_password_mismatch():
    """
    Test registration fails if password and confirmed_password do not match
    """
    client = APIClient()
    data = {
        "username": "user3",
        "password": "password123",
        "confirmed_password": "password456",
        "email": "user3@example.com"
    }
    response = client.post("/api/register/", data, format="json")
    assert response.status_code == 400

@pytest.mark.django_db
def test_register_existing_username():
    """
    Test registration fails if username already exists
    """
    User.objects.create_user(username="existinguser", password="12345")
    client = APIClient()
    data = {
        "username": "existinguser",
        "password": "newpassword",
        "confirmed_password": "newpassword",
        "email": "existinguser@example.com"
    }
    response = client.post("/api/register/", data, format="json")
    assert response.status_code == 400
