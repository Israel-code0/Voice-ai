# Voice AI

A personal voice-controlled AI assistant for Windows.

## Current Features

- Speech-to-text using Whisper
- Microphone input
- Open Windows applications
- Keyboard control
- Mouse control
- Open websites
- Basic voice command processing

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
