from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer
from .authentication import CookieRefreshAuthentication

class RegistrationView(APIView):
    """
    API view for user registration.

    Handles POST requests to create a new user. Uses the
    RegistrationSerializer to validate input data and create
    the user.

    Methods:
        post(request):
            Accepts username, email, password, and confirmed_password.
            Returns HTTP 201 on successful registration or
            HTTP 400 if validation fails.
    """

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CookieTokenObtainPairView(TokenObtainPairView):
    """
    API view for user login that issues JWT tokens and sets them as cookies.

    Extends TokenObtainPairView from SimpleJWT. On successful login,
    sets 'access_token' and 'refresh_token' cookies and returns
    basic user info.

    Methods:
        post(request, *args, **kwargs):
            Accepts username and password.
            Sets 'access_token' and 'refresh_token' cookies on the response.
            Returns user info and login detail.
    """
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")
        access = response.data.get("access")

        response.set_cookie(
            key="access_token",
            value = access,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.set_cookie(
            key="refresh_token",
            value = refresh,
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        response.data = {
            "detail": "Login successfully",
            "user":{
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
        return response

class CookieTokenRefreshView(APIView):
    """
    API view to refresh the access token using a refresh token from cookies.

    Uses the custom CookieRefreshAuthentication to extract the refresh token
    from the request cookies. Returns a new access token and sets it as a cookie.

    Attributes:
        authentication_classes: Uses CookieRefreshAuthentication.
        permission_classes: Requires the user to be authenticated via refresh token.

    Methods:
        post(request):
            Reads the refresh token from cookies.
            Returns a new access token if the refresh token is valid.
            Returns HTTP 401 if refresh token is missing or invalid.
    """
    authentication_classes = [CookieRefreshAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
       
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token  

            response = Response(
                {"detail": "Token refreshed", "access": str(access)},
                status=status.HTTP_200_OK
            )

        
            response.set_cookie(
                key="access_token",
                value=str(access),
                httponly=True,
                secure=True,  
                samesite="Lax"
            )

            return response

        except TokenError:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):
    """
    API view to log out the user and invalidate all tokens.

    Reads the refresh token from cookies and attempts to blacklist it.
    Deletes both 'access_token' and 'refresh_token' cookies on the client.

    Methods:
        post(request):
            Invalidates the refresh token if it exists.
            Deletes token cookies and returns a success message.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # funktioniert nur, wenn token noch nicht geblacklistet
            except TokenError:
                pass

        response = Response(
            {"detail": "Log-Out successfully! All Tokens will be deleted. Refresh token is now invalid."},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
