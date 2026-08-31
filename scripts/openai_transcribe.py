"""Manual check: transcribe a recording with the OpenAI Whisper API.

Requires OPENAI_API_KEY. The main assistant uses local faster-whisper instead.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sounddevice as sd  # noqa: E402
from scipy.io.wavfile import write  # noqa: E402
from openai import OpenAI  # noqa: E402

import config  # noqa: E402


def get_client():

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Add it to your .env file."
        )

    return OpenAI(api_key=api_key)


def record_audio(filename="command.wav", duration=5):

    print("🎙️ Listening...")

    recording = sd.rec(
        int(duration * config.SAMPLE_RATE),
        samplerate=config.SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=config.MICROPHONE_DEVICE
    )

    sd.wait()

    write(filename, config.SAMPLE_RATE, recording)

    print("Recording finished.")

    return filename


def transcribe_audio(filename="command.wav", client=None):

    client = client or get_client()

    with open(filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    return transcription.text


def main():

    client = get_client()

    filename = record_audio()

    print("You said:", transcribe_audio(filename, client=client))


if __name__ == "__main__":
    main()
