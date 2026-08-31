"""Microphone recording and Whisper transcription."""

import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

import config


class SpeechToText:
    """Records from the microphone and transcribes with faster-whisper.

    The model is loaded on first use so importing this module stays cheap.
    """

    def __init__(self, device=None, model_size=None):

        self.device = config.MICROPHONE_DEVICE if device is None else device
        self.model_size = model_size or config.WHISPER_MODEL
        self._model = None

    @property
    def model(self):

        if self._model is None:

            print("🧠 Loading voice recognition...")

            self._model = WhisperModel(
                self.model_size,
                device=config.WHISPER_DEVICE,
                compute_type=config.WHISPER_COMPUTE_TYPE
            )

            print("✅ Voice recognition ready.")

        return self._model

    def record(self, filename=None, duration=None):
        """Record audio to a wav file. Returns the path, or None on failure."""

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

        write(filename, config.SAMPLE_RATE, recording)

        return filename

    def transcribe(self, filename=None):
        """Transcribe a wav file."""

        filename = filename or config.RECORDING_FILE

        print("🧠 Understanding...")

        segments, _info = self.model.transcribe(filename, beam_size=5)

        return "".join(segment.text for segment in segments).strip()

    def listen(self):
        """Record a command and return the transcribed text."""

        filename = self.record()

        if filename is None:
            return ""

        return self.transcribe(filename)
