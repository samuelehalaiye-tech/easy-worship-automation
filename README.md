# Easy Whisper

Voice-to-text automation: send in audio, get back a transcript.

Easy Whisper is a small FastAPI service that wraps [Moonshine](https://github.com/moonshine-ai/moonshine), an open-source speech-to-text model built to run quickly on modest hardware. The model runs on your own machine, so no audio is sent to a third-party transcription service and no API key is needed.

<!-- Add a screenshot or short GIF of a transcription running. -->

## Features

- Transcribes audio through a simple HTTP API
- Runs the speech-to-text model locally, with no external service or API key
- Small and easy to extend, so the transcript can be passed to whatever comes next (saving it, searching it, summarising it)

## Tech stack

| Component | Technology |
|---|---|
| API | Python, FastAPI |
| Speech-to-text | Moonshine |

## Usage

Start the server (see below), then send an audio file:

```bash
curl -X POST http://localhost:8000/transcribe \
  -F "file=@sample.wav"
```

Example response:

```json
{ "text": "the transcript of your audio appears here" }
```

FastAPI also generates interactive docs at `http://localhost:8000/docs`, where you can try the API from your browser.

## Running locally

```bash
git clone https://github.com/samuelehalaiye-tech/easy-whisper.git
cd easy-whisper
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Notes

- Speech-to-text quality and speed depend on the Moonshine model you load and on your machine.
- This project was built while I was learning to build APIs and work with speech models, so it is a compact reference rather than a production service.

## Author

Onaopemipo Samuel Ehalaiye · [GitHub](https://github.com/samuelehalaiye-tech) · [LinkedIn](https://www.linkedin.com/in/onaopemipo-ehalaiye-7b140b424/)
