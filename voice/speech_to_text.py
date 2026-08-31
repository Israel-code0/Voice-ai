"""Microphone recording and Whisper transcription.

Two backends are supported because `faster-whisper` depends on PyAV, whose
bundled DLLs are blocked by Windows Smart App Control on some machines:

- ``faster-whisper`` (default, fastest)
- ``whisper`` (openai-whisper, PyAV free)

Both are fed the recorded samples directly, so neither needs ffmpeg.
Set ``VOICE_AI_STT_BACKEND`` to force one; the default ``auto`` tries
faster-whisper first and falls back when its import fails.
"""

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

import config


class FasterWhisperBackend:
    """faster-whisper (CTranslate2). Requires PyAV to import."""

    name = "faster-whisper"

    def __init__(self, model_size):

        from faster_whisper import WhisperModel

        self.model = WhisperModel(
            model_size,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE_TYPE
        )

    def transcribe(self, samples):

        segments, _info = self.model.transcribe(samples, beam_size=5)

        return "".join(segment.text for segment in segments).strip()


class OpenAIWhisperBackend:
    """openai-whisper. Slower, but does not import PyAV or shell out to ffmpeg."""

    name = "whisper"

    def __init__(self, model_size):

        import whisper

        self.model = whisper.load_model(model_size)

    def transcribe(self, samples):

        result = self.model.transcribe(samples, fp16=False)

        return result["text"].strip()


BACKENDS = {
    FasterWhisperBackend.name: FasterWhisperBackend,
    OpenAIWhisperBackend.name: OpenAIWhisperBackend
}


def load_backend(name, model_size):
    """Build the requested backend, or the first importable one for 'auto'."""

    if name != "auto":

        if name not in BACKENDS:
            raise ValueError(
                f"Unknown speech backend {name!r}. "
                f"Choose from: {', '.join(BACKENDS)}, auto."
            )

        return BACKENDS[name](model_size)

    errors = []

    for backend in BACKENDS.values():

        try:
            return backend(model_size)
        except (ImportError, OSError) as error:
            print(f"⚠️ {backend.name} unavailable: {error}")
            errors.append(f"{backend.name}: {error}")

    raise RuntimeError(
        "No speech recognition backend could be loaded.\n" + "\n".join(errors)
    )


def to_float32(samples):
    """Convert int16 PCM to the float32 range Whisper expects."""

    return samples.astype(np.float32).flatten() / 32768.0


class SpeechToText:
    """Records from the microphone and transcribes it.

    The model is loaded on first use so importing this module stays cheap.
    """

    def __init__(self, device=None, model_size=None, backend=None):

        self.device = config.MICROPHONE_DEVICE if device is None else device
        self.model_size = model_size or config.WHISPER_MODEL
        self.backend_name = backend or config.STT_BACKEND
        self._backend = None

    @property
    def backend(self):

        if self._backend is None:

            print("🧠 Loading voice recognition...")

            self._backend = load_backend(self.backend_name, self.model_size)

            print(f"✅ Voice recognition ready ({self._backend.name}).")

        return self._backend

    def record(self, filename=None, duration=None):
        """Record audio. Returns the samples, or None when recording failed."""

        filename = filename or config.RECORDING_FILE
        duration = duration or config.RECORDING_DURATION

        print()
        print("🎙️ Listening...")

        try:

            recording = sd.rec(
                int(duration * config.SAMPLE_RATE),
                samplerate=config.SAMPLE_RATE,
                channels=1,
                dtype="int16",
                device=self.device
            )

            sd.wait()

        except sd.PortAudioError as error:

            print(f"❌ Microphone error: {error}")
            print("Set VOICE_AI_MIC_DEVICE to a device index from:")
            print(sd.query_devices())

            return None

        if filename:
            write(filename, config.SAMPLE_RATE, recording)

        return recording

    def transcribe(self, samples):
        """Transcribe int16 samples recorded at config.SAMPLE_RATE."""

        print("🧠 Understanding...")

        return self.backend.transcribe(to_float32(samples))

    def listen(self):
        """Record a command and return the transcribed text."""

        samples = self.record()

        if samples is None:
            return ""

        return self.transcribe(samples)
