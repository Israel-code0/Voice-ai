"""Spoken responses using pyttsx3.

Speech is best effort: if no TTS voice is available the assistant keeps
working and only prints its replies.
"""

import config

try:
    import pyttsx3
except ImportError:  # pragma: no cover - optional dependency
    pyttsx3 = None


_engine = None


def get_engine():
    """Return a shared pyttsx3 engine, or None if TTS is unavailable."""

    global _engine

    if not config.SPEECH_ENABLED or pyttsx3 is None:
        return None

    if _engine is None:

        try:
            _engine = pyttsx3.init()
            _engine.setProperty("rate", config.SPEECH_RATE)
        except Exception as error:  # pragma: no cover - driver specific
            print(f"⚠️ Text to speech unavailable: {error}")
            return None

    return _engine


def speak(text):
    """Say text out loud (and always print it)."""

    print(f"🔊 {text}")

    engine = get_engine()

    if engine is None:
        return False

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as error:  # pragma: no cover - driver specific
        print(f"⚠️ Text to speech failed: {error}")
        return False

    return True
