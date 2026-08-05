import sys

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from asr import transcribe_audio
from llm import generate_reply
from tts import synthesize_speech

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI()


@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    user_text = transcribe_audio(audio_bytes)
    reply_text = generate_reply(user_text)
    audio_path = synthesize_speech(reply_text)
    print(f"user_text: {user_text}")
    print(f"reply_text: {reply_text}")
    return FileResponse(audio_path, media_type="audio/wav")
