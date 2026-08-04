import sys

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from asr import transcribe_audio

sys.stdout.reconfigure(encoding="utf-8")

app = FastAPI()


@app.post("/chat/")
async def chat_endpoint(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    user_text = transcribe_audio(audio_bytes)
    print(f"user_text: {user_text}")
    # TODO: LLM → TTS
    return FileResponse("response.wav", media_type="audio/wav")
