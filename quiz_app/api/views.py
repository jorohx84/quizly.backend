# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from .serializers import QuizCreateSerializer
# from quiz_app.models import Quiz, Question
# from .functions import download_audio, transcribe_audio, generate_quiz


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

#         video_url = serializer.validated_data.get("video_url")

#         try:
#             # 1️⃣ Audio herunterladen
#             audio_file = download_audio(video_url)

#             # 2️⃣ Transkribieren
#             transcript = transcribe_audio(audio_file) or ""

#             # 3️⃣ Quiz generieren
#             quiz_json, raw_text = generate_quiz(transcript)

#             # 4️⃣ Defensive Checks
#             if not quiz_json:
#                 return Response({
#                     "detail": "Gemini returned no data.",
#                     "raw_text": raw_text
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             title = quiz_json.get("title") or "Generated Quiz"
#             description = quiz_json.get("description") or ""
#             questions = quiz_json.get("questions") or []

#             if not questions:
#                 return Response({
#                     "detail": "Gemini returned no questions.",
#                     "raw_text": raw_text
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # 5️⃣ Quiz speichern
#             quiz = Quiz.objects.create(
#                 title=title,
#                 description=description,
#                 video_url=video_url
#             )

#             # 6️⃣ Fragen speichern
#             for q in questions:
#                 question_title = q.get("question_title") or "No title"
#                 options = q.get("question_options") or []
#                 answer = q.get("answer") or ""

#                 question = Question.objects.create(
#                     question_title=question_title,
#                     question_options=",".join(options),
#                     answer=answer
#                 )
#                 quiz.questions.add(question)  # nur bei ManyToManyField

#             # 7️⃣ Response vorbereiten
#             response_data = {
#                 "id": quiz.id,
#                 "title": quiz.title,
#                 "description": quiz.description,
#                 "video_url": quiz.video_url,
#                 "questions": [
#                     {
#                         "id": q.id,
#                         "question_title": q.question_title,
#                         "question_options": q.question_options.split(",") if q.question_options else [],
#                         "answer": q.answer
#                     } for q in quiz.questions.all()
#                 ]
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class QuizListView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         try:
#             # Alle Quizzes des authentifizierten Benutzers
#             quizzes = Quiz.objects.filter(user=request.user).prefetch_related("questions")

#             data = [
#                 {
#                     "id": quiz.id,
#                     "title": quiz.title,
#                     "description": quiz.description,
#                     "created_at": quiz.created_at,
#                     "updated_at": quiz.updated_at,
#                     "video_url": quiz.video_url,
#                     "questions": [
#                         {
#                             "id": q.id,
#                             "question_title": q.question_title,
#                             "question_options": q.question_options.split(","),
#                             "answer": q.answer
#                         }
#                         for q in quiz.questions.all()
#                     ]
#                 }
#                 for quiz in quizzes
#             ]

#             return Response(data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"detail": f"Internal Server Error: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
        

# class QuizDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         try:
#             # Versuche das Quiz zu laden
#             quiz = Quiz.objects.prefetch_related("questions").filter(id=id).first()

#             if not quiz:
#                 return Response(
#                     {"detail": "Quiz not found."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # Prüfe Besitzrecht
#             if quiz.user != request.user:
#                 return Response(
#                     {"detail": "Access denied - this quiz does not belong to you."},
#                     status=status.HTTP_403_FORBIDDEN,
#                 )

#             # Quiz-Daten strukturieren
#             data = {
#                 "id": quiz.id,
#                 "title": quiz.title,
#                 "description": quiz.description,
#                 "created_at": quiz.created_at,
#                 "updated_at": quiz.updated_at,
#                 "video_url": quiz.video_url,
#                 "questions": [
#                     {
#                         "id": q.id,
#                         "question_title": q.question_title,
#                         "question_options": q.question_options.split(","),
#                         "answer": q.answer,
#                     }
#                     for q in quiz.questions.all()
#                 ],
#             }

#             return Response(data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response(
#                 {"detail": f"Internal Server Error: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from .serializers import QuizCreateSerializer, QuizSerializer
from quiz_app.models import Quiz
from .functions import download_audio, transcribe_audio, generate_quiz


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
            audio_file = download_audio(video_url)
            transcript = transcribe_audio(audio_file) or ""
            quiz_json, raw_text = generate_quiz(transcript)

            if not quiz_json or not quiz_json.get("questions"):
                return Response({
                    "detail": "Failed to generate quiz.",
                    "raw_text": raw_text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            quiz = Quiz.objects.create(
                title=quiz_json.get("title", "Generated Quiz"),
                description=quiz_json.get("description", ""),
                video_url=video_url,
                user=request.user  # ✅ Besitzer setzen
            )

            # Fragen hinzufügen
            for q in quiz_json["questions"]:
                quiz.questions.create(
                    question_title=q.get("question_title", "No title"),
                    question_options=";".join(q.get("question_options", [])),
                    answer=q.get("answer", "")
                )

            # Serializer für Ausgabe
            output_serializer = QuizSerializer(quiz)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuizListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        quizzes = Quiz.objects.filter(user=request.user).prefetch_related("questions")
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class QuizDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, id):
#         try:
#             quiz = Quiz.objects.prefetch_related("questions").filter(id=id).first()
#             if not quiz:
#                 return Response({"detail": "Quiz not found."}, status=status.HTTP_404_NOT_FOUND)
#             if quiz.user != request.user:
#                 return Response({"detail": "Access denied."}, status=status.HTTP_403_FORBIDDEN)

#             serializer = QuizSerializer(quiz)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET     /api/quizzes/<id>/   -> Quiz abrufen
    PUT     /api/quizzes/<id>/   -> Quiz komplett updaten
    PATCH   /api/quizzes/<id>/   -> Quiz teilweise updaten
    DELETE  /api/quizzes/<id>/   -> Quiz löschen
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Nur Quizzes zurückgeben, die dem angemeldeten Benutzer gehören.
        """
        return self.queryset.filter(user=self.request.user)