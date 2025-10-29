from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import QuizCreateSerializer, QuizSerializer
from quiz_app.models import Quiz
from .functions import create_quiz_from_video


class CreateQuizView(APIView):
    """
    API endpoint for creating a new quiz based on a provided video URL.

    This view requires authentication. It expects a POST request containing
    a valid video URL, from which a quiz will be generated using the
    `create_quiz_from_video` utility.

    Methods:
        post(request):
            Validate the input data, generate a quiz, and return the created quiz data.

    Permissions:
        - IsAuthenticated: Only authenticated users can create quizzes.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuizCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_url = serializer.validated_data["url"]

        try:
            quiz = create_quiz_from_video(video_url, request.user)
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class QuizListView(APIView):
    """
    API endpoint for listing all quizzes created by the authenticated user.

    This view returns a list of quizzes associated with the current user,
    including their related questions. It supports only GET requests.

    Methods:
        get(request):
            Retrieve all quizzes belonging to the authenticated user.

    Permissions:
        - IsAuthenticated: Only authenticated users can view their quizzes.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user).prefetch_related("questions")
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, or deleting a specific quiz.

    This view allows authenticated users to access only their own quizzes.
    It provides full CRUD operations (retrieve, update, delete) for a quiz instance.

    Methods:
        get_object():
            Ensures that the requested quiz belongs to the authenticated user.
            Raises a PermissionDenied exception if the user does not own the quiz.

    Permissions:
        - IsAuthenticated: Only authenticated users can access this endpoint.
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise exceptions.PermissionDenied("You do not have permission to access this quiz.")
        return obj
    