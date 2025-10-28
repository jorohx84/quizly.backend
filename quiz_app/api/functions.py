# from yt_dlp import YoutubeDL
from google import genai
from ..models import Quiz
from .utils import clean_gemini_json, download_audio, transcribe_audio
# import whisper
import json
# import re
import os

# Whisper-Modell einmal laden
# _whisper_model = whisper.load_model("base")

# Gemini Client vorbereiten
client = genai.Client(api_key="AIzaSyDZt3P8I-_pdLH7L4aQvx8qmrTwgvMVeYk")
import os

# from yt_dlp import YoutubeDL


# def download_audio(youtube_url, output_path="audio.mp3"):
#     """
#     Lädt Audio eines YouTube-Videos herunter und gibt den Pfad zur MP3 zurück.
#     """
#     if not youtube_url:
#         raise ValueError("No YouTube URL provided.")

#     base_name = os.path.splitext(output_path)[0]  # -> "audio"
#     output_template = f"{base_name}.%(ext)s"

#     ydl_opts = {
#         "format": "bestaudio/best",
#         "outtmpl": output_template,
#         "postprocessors": [{
#             "key": "FFmpegExtractAudio",
#             "preferredcodec": "mp3",
#         }],
#         "quiet": False,
#         "no_warnings": True,
#     }

#     try:
#         with YoutubeDL(ydl_opts) as ydl:
#             ydl.download([youtube_url])

#         # Prüfen, welches File erzeugt wurde (mp3)
#         if os.path.exists(f"{base_name}.mp3"):
#             return f"{base_name}.mp3"
#         elif os.path.exists(f"{base_name}.mp3.mp3"):
#             # Fallback falls yt-dlp doppelt .mp3 angehängt hat
#             new_name = f"{base_name}.mp3"
#             os.rename(f"{base_name}.mp3.mp3", new_name)
#             return new_name
#         else:
#             raise FileNotFoundError(f"Audio file not found after download: {output_path}")

#     except Exception as e:
#         raise RuntimeError(f"Failed to download audio: {str(e)}")


# def transcribe_audio(file_path):
#     """
#     Transkribiert ein Audiofile mit Whisper und liefert den Text zurück.
#     """
#     if not file_path or not os.path.exists(file_path):
#         raise ValueError("Audio file path is invalid or does not exist.")

#     try:
#         result = _whisper_model.transcribe(file_path)
#         text = result.get("text") or ""
#         return text
#     except Exception as e:
#         raise RuntimeError(f"Failed to transcribe audio: {str(e)}")


# def clean_gemini_json(raw_text):
#     """
#     Entfernt ```json ... ``` Markup von Gemini-Ausgabe und gibt sauberes JSON zurück.
#     """
#     raw_text = raw_text or ""
#     match = re.search(r"```json(.*?)```", raw_text, re.DOTALL)
#     if match:
#         return match.group(1).strip()
#     return raw_text.strip()


# def generate_quiz(transcript):
#     """
#     Generiert ein Quiz aus dem Transkript mit Gemini.
#     Liefert ein dict (quiz_json) und den rohen Text (raw_text) zurück.
#     """
#     transcript = transcript or ""
#     prompt = f"""
#     Erstelle ein Quiz aus diesem Text auf Deutsch. 
#     Gib es als valides JSON zurück mit folgenden Feldern:
#     title, description, questions.
#     Jede Frage hat: question_title, question_options (Liste), answer
#     """

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=prompt + "\n" + transcript
#         )
#         raw_text = response.text or ""
#         clean_text = clean_gemini_json(raw_text)

#         # JSON parsen
#         try:
#             quiz_json = json.loads(clean_text)
#             # Defensive Checks
#             if not isinstance(quiz_json, dict):
#                 raise ValueError("Gemini returned JSON is not a dict.")
#             return quiz_json, raw_text
#         except Exception as parse_error:
#             raise ValueError(f"Gemini returned invalid JSON: {str(parse_error)}\nRaw Text: {raw_text}")

#     except Exception as e:
#         raise RuntimeError(f"Failed to generate quiz with Gemini: {str(e)}")
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
                # question_options=",".join(q.get("question_options", [])),
                question_options=q.get("question_options", []),
                answer=q.get("answer", "")
            )
        return quiz