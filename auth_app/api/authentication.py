from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the access token from cookies.

    Methods:
        get_header(request):
            Overrides the default method to return None because the token
            is retrieved from cookies, not from the Authorization header.

        authenticate(request):
            Retrieves the 'access_token' from cookies.
            Validates the token and returns a tuple (user, token) if valid.
            Raises AuthenticationFailed if the token is invalid.
    """
    def get_header(self, request):
      
        return None

    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken as e:
            raise AuthenticationFailed('Invalid token')

        return self.get_user(validated_token), validated_token

class CookieRefreshAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class for validating refresh tokens from cookies.

    Methods:
        authenticate(request):
            Retrieves the 'refresh_token' from cookies.
            Validates the token and returns a tuple (user, None) if valid.
            Returns None if no refresh token is provided.
            Raises AuthenticationFailed if the token is invalid or the user does not exist.
    """
    def authenticate(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return None  

        try:
            token = RefreshToken(refresh_token)
            user_id = token["user_id"]
            user = User.objects.get(id=user_id)
            return (user, None)
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid refresh token")