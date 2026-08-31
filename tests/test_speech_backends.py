"""Backend selection tests. No microphone, model or network needed."""

import io
import os
import sys
import types
import unittest
import wave

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sounddevice needs PortAudio, which headless machines do not have.
sys.modules.setdefault("sounddevice", types.ModuleType("sounddevice"))

try:
    import numpy as np
    from scipy.io.wavfile import write  # noqa: F401
except ImportError:  # pragma: no cover - dependencies not installed
    np = None

if np is not None:
    from voice import speech_to_text


BLOCKED = (
    "DLL load failed while importing hwaccel: "
    "An Application Control policy has blocked this file."
)


class _FakeLocalModel:

    def __init__(self, size):
        self.size = size

    def transcribe(self, samples, **_kwargs):
        return {"text": " Open Notepad. "}


class _FakeTranscriptions:

    def __init__(self):
        self.uploaded = None

    def create(self, model, file):

        self.uploaded = file.read()

        return types.SimpleNamespace(text=" Open Notepad. ")


class _FakeOpenAI:

    last = None

    def __init__(self, api_key):
        self.api_key = api_key
        self.audio = types.SimpleNamespace(transcriptions=_FakeTranscriptions())
        _FakeOpenAI.last = self


@unittest.skipIf(np is None, "numpy and scipy are required")
class BackendSelectionTests(unittest.TestCase):

    def setUp(self):

        self.original_modules = dict(sys.modules)
        self.addCleanup(self._restore_modules)

        # Windows Smart App Control blocks the DLLs both local models load.
        for name, symbol in (("faster_whisper", "WhisperModel"),
                             ("whisper", "load_model")):

            module = types.ModuleType(name)

            def blocked(*_args, **_kwargs):
                raise ImportError(BLOCKED)

            setattr(module, symbol, blocked)
            sys.modules[name] = module

        openai_module = types.ModuleType("openai")
        openai_module.OpenAI = _FakeOpenAI
        sys.modules["openai"] = openai_module

        self.original_key = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = "test-key"
        self.addCleanup(self._restore_key)

    def _restore_modules(self):

        sys.modules.clear()
        sys.modules.update(self.original_modules)

    def _restore_key(self):

        if self.original_key is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = self.original_key

    def test_auto_falls_back_to_the_api_when_both_models_are_blocked(self):

        backend = speech_to_text.load_backend("auto", "base")

        self.assertEqual(backend.name, "openai")

    def test_auto_prefers_a_local_model_when_one_loads(self):

        sys.modules["whisper"].load_model = _FakeLocalModel

        backend = speech_to_text.load_backend("auto", "base")

        self.assertEqual(backend.name, "whisper")

    def test_auto_skips_the_api_without_a_key(self):

        os.environ.pop("OPENAI_API_KEY")

        with self.assertRaises(RuntimeError):
            speech_to_text.load_backend("auto", "base")

    def test_forced_backend_reports_why_it_failed(self):

        with self.assertRaises(ImportError):
            speech_to_text.load_backend("faster-whisper", "base")

    def test_unknown_backend_name_is_rejected(self):

        with self.assertRaises(ValueError):
            speech_to_text.load_backend("nope", "base")

    def test_api_backend_uploads_a_playable_wav(self):

        backend = speech_to_text.load_backend("openai", "base")

        text = backend.transcribe(np.zeros((160, 1), dtype=np.int16))

        self.assertEqual(text, "Open Notepad.")

        uploaded = _FakeOpenAI.last.audio.transcriptions.uploaded

        with wave.open(io.BytesIO(uploaded)) as wav:
            self.assertEqual(wav.getnchannels(), 1)
            self.assertEqual(wav.getsampwidth(), 2)
            self.assertEqual(wav.getnframes(), 160)


@unittest.skipIf(np is None, "numpy and scipy are required")
class SampleConversionTests(unittest.TestCase):

    def test_int16_samples_become_flat_float32(self):

        samples = np.array([[0], [32767], [-32768]], dtype=np.int16)

        converted = speech_to_text.to_float32(samples)

        self.assertEqual(converted.dtype, np.float32)
        self.assertEqual(converted.shape, (3,))
        self.assertAlmostEqual(float(converted[1]), 1.0, places=4)
        self.assertAlmostEqual(float(converted[2]), -1.0, places=4)


if __name__ == "__main__":
    unittest.main()
