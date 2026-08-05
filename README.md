# Voice Agent

A FastAPI-based voice agent: it takes an audio clip, transcribes it to text, feeds it to an LLM to generate a reply, and synthesizes that reply back into speech. Overall pipeline:

```
Audio input → ASR (speech recognition) → LLM (reply generation) → TTS (speech synthesis) → Audio output
```

## Modules

| Module | File | Description |
|---|---|---|
| API server | `main.py` | FastAPI app exposing `POST /chat/`, chaining the ASR → LLM → TTS pipeline |
| Speech recognition (ASR) | `asr.py` | Transcribes the uploaded audio using OpenAI Whisper (`small` model). Language is forced to English to avoid short clips being misdetected as another language |
| Reply generation (LLM) | `llm.py` | Calls Agnes AI (a third-party service compatible with the OpenAI Chat Completions API) to generate a reply. Persona is a witty, joke-loving assistant, with a rolling 5-turn conversation memory |
| Speech synthesis (TTS) | `tts.py` | Synthesizes the reply text into speech using `pyttsx3` (local, offline, backed by the system's SAPI5 engine) |

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root (already git-ignored, never committed):

```
AGNES_API_KEY=your_agnes_ai_api_key
```

## Run

```bash
uvicorn main:app --reload
```

The server listens on `http://127.0.0.1:8000`.

## API Usage

```bash
curl -X POST http://127.0.0.1:8000/chat/ \
  -F "file=@your_audio.mp3" \
  -o response.wav
```

Request: upload an audio file (form field name `file`)
Response: the synthesized reply audio (`audio/wav`)

## Project Structure

```
voice_agent/
├── main.py              # FastAPI entry point, /chat/ endpoint
├── asr.py                # Speech recognition (Whisper)
├── llm.py                 # Reply generation (Agnes AI)
├── tts.py                 # Speech synthesis (pyttsx3)
├── requirements.txt
├── .env                    # API key (local only, never committed)
└── tests/
    ├── fixtures/            # Sample audio used for testing
    └── results/              # Per-step test artifacts (server logs, transcripts, response audio)
```

## Known Issues

- **Empty transcription causes a 500 error**: if the uploaded audio is silent/invalid, Whisper transcribes it as an empty string, and Agnes AI's API returns 400 because the message content is empty. This isn't currently handled, so it surfaces to the client as an unhandled 500.
