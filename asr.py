import whisper

_model = whisper.load_model("small")


def transcribe_audio(audio_bytes: bytes) -> str:
    with open("temp.wav", "wb") as f:
        f.write(audio_bytes)
    # Force English: on short clips, Whisper's auto language-detection
    # (based on the first ~30s of log-mel spectrogram) can misidentify
    # the language, e.g. an English clip getting classified as Chinese.
    result = _model.transcribe("temp.wav", language="en")
    return result["text"]
