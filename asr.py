import whisper

_model = whisper.load_model("small")


def transcribe_audio(audio_bytes: bytes) -> str:
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    result = _model.transcribe("temp.wav")
    return result["text"]
