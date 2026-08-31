import os

import sounddevice as sd
from scipy.io.wavfile import write
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SAMPLE_RATE = 16000


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
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(filename, SAMPLE_RATE, recording)

    print("Recording finished.")


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

    record_audio()

    print("You said:", transcribe_audio(client=client))


if __name__ == "__main__":
    main()
