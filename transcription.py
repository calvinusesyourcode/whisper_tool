import os, openai, whisper, pathlib
from secret import secret

def transcribe_via_api(filename):
    openai.api_key = secret
    os.environ["REQUESTS_CA_BUNDLE"] = "C:/Users/calvi/3D Objects/test/Baltimore CyberTrust Root.crt"
    
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def transcribe_offline(model:str, file_path:pathlib.WindowsPath):
    """
| Model Size | Parameters | English-only | VRAM   | Relative Speed |
|------------|------------|--------------|--------|----------------|
| tiny       | 39 M       | tiny.en      | ~1 GB  | ~32x           |
| base       | 74 M       | base.en      | ~1 GB  | ~16x           |
| small      | 244 M      | small.en     | ~2 GB  | ~6x            |
| medium     | 769 M      | medium.en    | ~5 GB  | ~2x            |
| large      | 1550 M     | N/A          | ~10 GB | 1x             |
"""
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result
