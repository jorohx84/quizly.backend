from yt_dlp import YoutubeDL
from google import genai
import whisper
import re
import os


_whisper_model = whisper.load_model("base")

client = genai.Client(api_key="AIzaSyDZt3P8I-_pdLH7L4aQvx8qmrTwgvMVeYk")

from yt_dlp import YoutubeDL
import os


def download_audio(youtube_url, output_path="audio.mp3"):
    """
    downloads audio from a YouTube video and returns the path to the MP3.
    """
    if not youtube_url:
        raise ValueError("No YouTube URL provided.")

    base_name = os.path.splitext(output_path)[0]
    output_template = f"{base_name}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        _run_ydl(youtube_url, ydl_opts)
        return _resolve_audio_file(base_name)
    except Exception as e:
        raise RuntimeError(f"Failed to download audio: {e}")


def _run_ydl(url, opts):
    """
    runs yt-dlp download.
    """
    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def _resolve_audio_file(base_name):
    """
    checks which MP3 file was created and returns the path.
    """
    candidates = [f"{base_name}.mp3", f"{base_name}.mp3.mp3"]
    for file in candidates:
        if os.path.exists(file):
            if file.endswith(".mp3.mp3"):
                new_name = f"{base_name}.mp3"
                os.rename(file, new_name)
                return new_name
            return file
    raise FileNotFoundError(f"Audio file not found: {base_name}.mp3")


def transcribe_audio(file_path):
    """
    transcribes an audio file with Whisper and returns the text.
    """
    if not file_path or not os.path.exists(file_path):
        raise ValueError("Audio file path is invalid or does not exist.")

    try:
        result = _whisper_model.transcribe(file_path)
        text = result.get("text") or ""
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe audio: {str(e)}")


def clean_gemini_json(raw_text):
    """
    strips ```json ... ``` markup from Gemini output and returns clean JSON.
    """
    raw_text = raw_text or ""
    match = re.search(r"```json(.*?)```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_text.strip()