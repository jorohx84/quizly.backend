from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import QuizCreateSerializer, QuizSerializer
from quiz_app.models import Quiz
from .functions import create_quiz_from_video


# class CreateQuizView(APIView):
#     """
#     POST /api/createQuiz/
#     Erstellt ein neues Quiz basierend auf einer YouTube-URL.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = QuizCreateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         video_url = serializer.validated_data["video_url"]

#         try:
#             audio_file = download_audio(video_url)
#             transcript = transcribe_audio(audio_file) or ""
#             quiz_json, raw_text = generate_quiz(transcript)

#             if not quiz_json or not quiz_json.get("questions"):
#                 return Response({
#                     "detail": "Failed to generate quiz.",
#                     "raw_text": raw_text
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             quiz = Quiz.objects.create(
#                 title=quiz_json.get("title", "Generated Quiz"),
#                 description=quiz_json.get("description", ""),
#                 video_url=video_url,
#                 user=request.user  # ✅ Besitzer setzen
#             )

#             # Fragen hinzufügen
#             for q in quiz_json["questions"]:
#                 quiz.questions.create(
#                     question_title=q.get("question_title", "No title"),
#                     question_options=";".join(q.get("question_options", [])),
#                     answer=q.get("answer", "")
#                 )

#             # Serializer für Ausgabe
#             output_serializer = QuizSerializer(quiz)
#             return Response(output_serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateQuizView(APIView):
    """
    POST /api/createQuiz/
    Erstellt ein neues Quiz basierend auf einer YouTube-URL.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuizCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_url = serializer.validated_data["video_url"]

        try:
            quiz = create_quiz_from_video(video_url, request.user)
            return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class QuizListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user).prefetch_related("questions")
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise exceptions.PermissionDenied("You do not have permission to access this quiz.")
        return obj
    