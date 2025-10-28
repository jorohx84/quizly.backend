import pytest
from unittest.mock import patch, MagicMock
from quiz_app.api.utils import download_audio, _resolve_audio_file, transcribe_audio, clean_gemini_json

# --- download_audio / _resolve_audio_file ---
@pytest.mark.parametrize("url, expected_exception", [
    (None, ValueError),
    ("", ValueError),
])
def test_download_audio_invalid_url(url, expected_exception):
    with pytest.raises(expected_exception):
        download_audio(url)

@patch("quiz_app.api.utils._run_ydl")
@patch("quiz_app.api.utils._resolve_audio_file", return_value="audio.mp3")
def test_download_audio_success(mock_resolve, mock_run):
    result = download_audio("https://youtube.com/testvideo")
    mock_run.assert_called_once()
    mock_resolve.assert_called_once()
    assert result == "audio.mp3"

# --- _resolve_audio_file ---
@patch("os.path.exists", side_effect=[False, True])
@patch("os.rename")
def test_resolve_audio_file(mock_rename, mock_exists):
    from quiz_app.api.utils import _resolve_audio_file
    result = _resolve_audio_file("audio")
    mock_rename.assert_called_once()
    assert result == "audio.mp3"

# --- transcribe_audio ---
@patch("quiz_app.api.utils._whisper_model")
def test_transcribe_audio(mock_model):
    mock_model.transcribe.return_value = {"text": "hello world"}
    result = transcribe_audio("audio.mp3")
    mock_model.transcribe.assert_called_once_with("audio.mp3")
    assert result == "hello world"

def test_transcribe_audio_invalid_path():
    import os
    with pytest.raises(ValueError):
        transcribe_audio("non_existent_file.mp3")

# --- clean_gemini_json ---
def test_clean_gemini_json_with_json_block():
    raw = "Some text ```json {\"key\": 1} ``` more text"
    result = clean_gemini_json(raw)
    assert result == '{"key": 1}'

def test_clean_gemini_json_no_block():
    raw = "Just some text"
    result = clean_gemini_json(raw)
    assert result == "Just some text"
