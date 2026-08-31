"""Manual check: list input devices, record five seconds and transcribe."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sounddevice as sd  # noqa: E402

from voice.speech_to_text import SpeechToText  # noqa: E402


def main():

    print("Available devices:")
    print(sd.query_devices())

    text = SpeechToText().listen()

    print()
    print("You said:")
    print(text)


if __name__ == "__main__":
    main()
