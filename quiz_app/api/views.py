from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuizCreateSerializer
from quiz_app.models import Quiz, Question
from .functions import download_audio, transcribe_audio, generate_quiz


class CreateQuizView(APIView):
    """
    POST /api/createQuiz/
    Erstellt ein neues Quiz basierend auf einer YouTube-URL.
    """

    def post(self, request):
        serializer = QuizCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        video_url = serializer.validated_data.get("video_url")

        try:
            # 1️⃣ Audio herunterladen
            audio_file = download_audio(video_url)

            # 2️⃣ Transkribieren
            transcript = transcribe_audio(audio_file) or ""

            # 3️⃣ Quiz generieren
            quiz_json, raw_text = generate_quiz(transcript)

            # 4️⃣ Defensive Checks
            if not quiz_json:
                return Response({
                    "detail": "Gemini returned no data.",
                    "raw_text": raw_text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            title = quiz_json.get("title") or "Generated Quiz"
            description = quiz_json.get("description") or ""
            questions = quiz_json.get("questions") or []

            if not questions:
                return Response({
                    "detail": "Gemini returned no questions.",
                    "raw_text": raw_text
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 5️⃣ Quiz speichern
            quiz = Quiz.objects.create(
                title=title,
                description=description,
                video_url=video_url
            )

            # 6️⃣ Fragen speichern
            for q in questions:
                question_title = q.get("question_title") or "No title"
                options = q.get("question_options") or []
                answer = q.get("answer") or ""

                question = Question.objects.create(
                    question_title=question_title,
                    question_options=",".join(options),
                    answer=answer
                )
                quiz.questions.add(question)  # nur bei ManyToManyField

            # 7️⃣ Response vorbereiten
            response_data = {
                "id": quiz.id,
                "title": quiz.title,
                "description": quiz.description,
                "video_url": quiz.video_url,
                "questions": [
                    {
                        "id": q.id,
                        "question_title": q.question_title,
                        "question_options": q.question_options.split(",") if q.question_options else [],
                        "answer": q.answer
                    } for q in quiz.questions.all()
                ]
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import QuizCreateSerializer
# from quiz_app.models import Quiz, Question
# from .functions import download_audio, transcribe_audio, generate_quiz


# class CreateQuizView(APIView):
#     def post(self, request):
#         serializer = QuizCreateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         video_url = serializer.validated_data["video_url"]

#         try:
#             audio_file = download_audio(video_url)
#             transcript = transcribe_audio(audio_file)
#             quiz_json, raw_text = generate_quiz(transcript)

#             if not quiz_json or "questions" not in quiz_json or not quiz_json["questions"]:
#                 return Response({
#                     "detail": "Gemini returned invalid or empty questions.",
#                     "raw_text": raw_text
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             quiz = Quiz.objects.create(
#                 title=quiz_json.get("title", "Generated Quiz"),
#                 description=quiz_json.get("description", ""),
#                 video_url=video_url
#             )

#             for q in quiz_json["questions"]:
#                 question = Question.objects.create(
#                     question_title=q["question_title"],
#                     question_options=",".join(q["question_options"]),
#                     answer=q["answer"]
#                 )
#                 quiz.questions.add(question)

#             response_data = {
#                 "id": quiz.id,
#                 "title": quiz.title,
#                 "description": quiz.description,
#                 "video_url": quiz.video_url,
#                 "questions": [
#                     {
#                         "id": q.id,
#                         "question_title": q.question_title,
#                         "question_options": q.question_options.split(","),
#                         "answer": q.answer
#                     } for q in quiz.questions.all()
#                 ]
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# import json
# import re
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import QuizCreateSerializer
# from quiz_app.models import Quiz, Question
# from google import genai
# import yt_dlp
# from whisper import load_model

# whisper_model = load_model("base")
# gemini_client = genai.Client(api_key="AIzaSyDZt3P8I-_pdLH7L4aQvx8qmrTwgvMVeYk")


# class CreateQuizView(APIView):
#     def post(self, request):
#         serializer = QuizCreateSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         video_url = serializer.validated_data["video_url"]

#         # 1️⃣ Audio von YouTube runterladen
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'outtmpl': 'temp_audio.%(ext)s',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }],
#         }

#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([video_url])
#             audio_file = "temp_audio.mp3"
#         except Exception as e:
#             return Response({"detail": f"YouTube download failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

#         # 2️⃣ Whisper Transkription
#         try:
#             result = whisper_model.transcribe(audio_file)
#             transcript = result["text"]
#         except Exception as e:
#             return Response({"detail": f"Whisper transcription failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # 3️⃣ Quiz von Gemini generieren
#         prompt = (
#             f"Erstelle ein Quiz aus diesem Text. Gib es als JSON zurück mit title, description und questions:\n\n{transcript}"
#         )
#         try:
#             gemini_response = gemini_client.models.generate_content(
#                 model="gemini-2.5-flash",
#                 contents=prompt
#             )
#             raw_text = gemini_response.text

#             # Codeblocks entfernen
#             cleaned_text = re.sub(r"```(?:json)?\s*(.*?)```", r"\1", raw_text, flags=re.DOTALL).strip()

#             # JSON parsen
#             try:
#                 quiz_json = json.loads(cleaned_text)
#             except json.JSONDecodeError:
#                 # Versuch, einfache Reparatur: alles nach erster { bis letzte } extrahieren
#                 match = re.search(r"{.*}", cleaned_text, flags=re.DOTALL)
#                 if match:
#                     quiz_json = json.loads(match.group(0))
#                 else:
#                     return Response({
#                         "detail": "Gemini returned invalid JSON.",
#                         "raw_text": raw_text
#                     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # Prüfen, ob Fragen existieren
#             questions = quiz_json.get("questions")
#             if not questions or not isinstance(questions, list):
#                 return Response({
#                     "detail": "Gemini hat keine Fragen generiert.",
#                     "raw_text": raw_text
#                 }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         except Exception as e:
#             return Response({"detail": f"Gemini generation failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # 4️⃣ Quiz + Fragen speichern
#         quiz = Quiz.objects.create(
#             title=quiz_json.get("title", "Generated Quiz"),
#             description=quiz_json.get("description", ""),
#             video_url=video_url
#         )

#         for q in questions:
#             if not all(k in q for k in ("question_title", "question_options", "answer")):
#                 continue
#             question = Question.objects.create(
#                 question_title=q["question_title"],
#                 question_options=",".join(q["question_options"]),
#                 answer=q["answer"]
#             )
#             quiz.questions.add(question)

#         # 5️⃣ Response vorbereiten
#         response_data = {
#             "id": quiz.id,
#             "title": quiz.title,
#             "description": quiz.description,
#             "video_url": quiz.video_url,
#             "questions": [
#                 {
#                     "id": q.id,
#                     "question_title": q.question_title,
#                     "question_options": q.question_options.split(","),
#                     "answer": q.answer
#                 } for q in quiz.questions.all()
#             ]
#         }

#         return Response(response_data, status=status.HTTP_201_CREATED)
