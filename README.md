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

## 🧩 Install FFmpeg (Required for Audio Transcription)
### Linux / MacOs
```bash
brew install ffmpeg 
```

### Windows
1.  Download:
```bash
 https://ffmpeg.org/download.html
```

## 🪐 Gemini AI Setup

### Get a Gemini API key:
   
Sign up and generate an API key here: 🪐 [Gemini Developer API](https://ai.google.dev/)  

   
#### 🔐 Environment Variables (Storing Your API Keys)

To keep your API keys secure and out of the source code, this project uses a **`.env` file**.  
You should never hard-code secrets like API keys directly into Python files or commit them to GitHub.

---

### ⚙️ Create a `.env` file

In the **root directory** of your Django project (next to `manage.py`), create a file named `.env`:


### Add your API key to your .env-file:

```bash
GOOGLE_GENAI_API_KEY=your-google-genai-api-key-here

```
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

---
🏃 Running the Project

### Start the Django server:
```bash
python manage.py runserver
```



