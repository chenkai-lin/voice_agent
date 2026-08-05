import pyttsx3


def synthesize_speech(text: str, output_path: str = "response.wav") -> str:
    # Create a fresh engine per call: reusing one engine across multiple
    # runAndWait() calls is a known source of hangs/silent failures in pyttsx3.
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()
    return output_path
