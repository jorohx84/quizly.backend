# 🎯 Quizly Backend

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PyPI](https://img.shields.io/pypi/v/google-genai?label=Google%20GenAI)](https://pypi.org/project/google-genai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Backend for the **Quizly** project, providing APIs and functionality for quiz management.

- 🤖 **Whisper AI** for audio transcription
- 🪐 **Gemini AI** for generative content
- 🎬 **FFmpeg** for audio/video processing

---

## ⚡ Prerequisites

- Python 3.13+
- Git
- Homebrew (macOS only)
- Virtual environment (recommended)

---

## 🚀 Installation

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/quizly.backend.git
```
```bash
cd quizly.backend
```

### 2. Create and activate a virtual environment:

```bash
python3 -m venv env
```
```bash
source env/bin/activate   # macOS/Linux
```
```bash
env\Scripts\activate      # Windows
```
### 3. Install dependencies:
```bash
pip install -r requirements.txt

```
---

## 🗄 Database Setup

### 1. Create migrations and migrate:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

### 2. Optionally, create a superuser:

```bash
python manage.py createsuperuser
```
---

## 🎤 Whisper AI Setup

### 1. Install Whisper AI:
   
```bash
pip install openai-whisper
```
### 2. Install FFmpeg:
   
```bash
brew install ffmpeg 
```

### 3. Example usage:

```bash
import whisper

model = whisper.load_model("base")
result = model.transcribe("audio.mp3")
print(result["text"])
```

---

🪐 Gemini AI Setup

### 1. Install Gemini AI SDK:
   
```bash
pip install google-genai
```
### 2. Get a Gemini API key:
   
Sign up and generate an API key here: 🪐 [Gemini Developer API](https://ai.google.dev/)  


### 4. Set your API key as an environment variable:
   
```bash
export GEMINI_API_KEY='your_api_key'
```

### 4. Example usage:
   
```bash
from google import genai

client = genai.Client(api_key='your_api_key')
response = client.generate("Say hello in German!")
print(response)
```

---
🏃 Running the Project

### Start the Django server:
```bash
python manage.py runserver
```



