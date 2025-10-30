from google import genai
from dotenv import load_dotenv
from ..models import Quiz
from .utils import clean_gemini_json, download_audio, transcribe_audio
import json
import os

# client = genai.Client(api_key="AIzaSyDZt3P8I-_pdLH7L4aQvx8qmrTwgvMVeYk")
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_GENAI_API_KEY in environment variables")

client = genai.Client(api_key=GOOGLE_API_KEY)

def generate_quiz(transcript):
    """
    Generates a quiz from the transcript in German and returns a dict and the raw text.
    """
    transcript = transcript or ""
    prompt = f""" Erstelle ein Quiz aus diesem Text auf Deutsch. Gib es als valides JSON zurück mit folgenden Feldern: title, description, questions. Jede Frage hat: question_title, question_options (Liste), answer. Es sollen immer exakt 4 Optionen erstellt werden. """
    try:
        raw_text = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt + "\n" + transcript
        ).text or ""
        quiz_json = json.loads(clean_gemini_json(raw_text))

        if not isinstance(quiz_json, dict) or not quiz_json.get("questions"):
            raise ValueError("Ungültiges Quiz-JSON.")

        return quiz_json, raw_text

    except Exception as e:
        raise RuntimeError(f"Fehler bei der Quiz-Generierung: {e}")


def create_quiz_from_video(video_url, user):
    """Pipeline: Download → Transkription → Quiz generieren → speichern"""
    audio_file = download_audio(video_url)
    transcript = transcribe_audio(audio_file) or ""
    quiz_json, raw_text = generate_quiz(transcript)
    validate_quiz_json(quiz_json, raw_text)
    return save_quiz(quiz_json, video_url, user)


def validate_quiz_json(quiz_json, raw_text):
        """
        Validates the generated quiz structure
        """
        if not quiz_json or not quiz_json.get("questions"):
            raise ValueError(f"Failed to generate quiz. Raw text: {raw_text}")


def save_quiz(quiz_json, video_url, user):
        """
        saves the quiz and its questions in the database
        """
        quiz = Quiz.objects.create(
            title=quiz_json.get("title", "Generated Quiz"),
            description=quiz_json.get("description", ""),
            video_url=video_url,
            user=user
        )
        for q in quiz_json["questions"]:
            quiz.questions.create(
                question_title=q.get("question_title", "No title"),
                question_options=q.get("question_options", []),
                answer=q.get("answer", "")
            )
        return quiz