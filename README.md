# Voice AI

A personal voice-controlled AI assistant for Windows.

## Current Features

- Speech-to-text using Whisper
- Microphone input
- Spoken responses (pyttsx3)
- Open Windows applications
- Keyboard control
- Mouse control
- Open websites
- Basic voice command processing

## Project Structure

```
main.py                     entry point: listen -> parse -> act
config.py                   settings, app and website tables
agent/brain.py              turns transcribed text into an Intent
agent/tools.py              maps intents onto the functions that run them
computer/applications.py    launching apps and websites
computer/keyboard.py        typing and key presses
computer/mouse.py           clicking and scrolling
voice/speech_to_text.py     microphone recording + Whisper
voice/text_to_speech.py     spoken replies
scripts/                    manual checks (microphone, OpenAI API)
tests/                      unit tests for the command grammar
```

`agent/brain.py` has no audio or GUI dependencies, so the command grammar can
be tested without a microphone:

```bash
python -m unittest discover -s tests
```

## Current Commands

Examples:

- Open Chrome
- Open Notepad
- Open Calculator
- Type Hello World
- Press Enter
- Press Space
- Go to Google
- Go to YouTube
- Go to GitHub
- Scroll down
- Scroll up
- Click
- Exit

## Technologies

- Python
- Faster Whisper
- SoundDevice
- PyAutoGUI
- SciPy

## Project Status

Early development.

The long-term goal is to create a voice AI capable of navigating and controlling a PC and mobile devices through natural language.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the assistant:

```bash
python main.py
```

## Configuration

Optional environment variables:

- `VOICE_AI_MIC_DEVICE` - input device index (defaults to the system default
  microphone). Run `python -c "import sounddevice; print(sounddevice.query_devices())"`
  to list the available devices.
- `VOICE_AI_WHISPER_MODEL` - Whisper model size, defaults to `base`.
- `OPENAI_API_KEY` - only needed by `voice.py` and `test_api.py`, read from a
  `.env` file.
