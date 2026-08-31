"""Voice AI entry point: listen -> parse -> act."""

from agent import tools
from agent.brain import parse_command
from voice.speech_to_text import SpeechToText
from voice.text_to_speech import speak


def banner():

    print()
    print("===================================")
    print("🎙️  VOICE AI")
    print("===================================")
    print("Speak a command...")
    print("Say 'exit' to stop.")


def main():

    ears = SpeechToText()
    registry = tools.build_tools()

    speak("Voice AI ready.")

    while True:

        banner()

        try:
            text = ears.listen()
        except KeyboardInterrupt:
            break

        print()
        print("You said:")
        print(text)

        intent = parse_command(text)

        if not tools.execute(intent, registry):
            break

    print()
    speak("Voice AI shutting down.")


if __name__ == "__main__":
    main()
