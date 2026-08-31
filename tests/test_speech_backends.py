"""Backend selection tests. No microphone or Whisper model needed."""

import os
import sys
import types
import unittest

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


@unittest.skipIf(np is None, "numpy and scipy are required")
class BackendSelectionTests(unittest.TestCase):

    def setUp(self):

        self.original = dict(sys.modules)
        self.addCleanup(self._restore)

        # Windows Smart App Control blocks the DLL PyAV loads.
        blocked = types.ModuleType("faster_whisper")

        def blocked_model(*_args, **_kwargs):
            raise ImportError(BLOCKED)

        blocked.WhisperModel = blocked_model
        sys.modules["faster_whisper"] = blocked

        whisper = types.ModuleType("whisper")
        whisper.load_model = lambda size: _FakeModel(size)
        sys.modules["whisper"] = whisper

    def _restore(self):

        sys.modules.clear()
        sys.modules.update(self.original)

    def test_auto_falls_back_when_faster_whisper_is_blocked(self):

        backend = speech_to_text.load_backend("auto", "base")

        self.assertEqual(backend.name, "whisper")

    def test_named_backend_is_used_as_is(self):

        backend = speech_to_text.load_backend("whisper", "base")

        self.assertEqual(backend.name, "whisper")

    def test_forced_backend_reports_why_it_failed(self):

        with self.assertRaises(ImportError):
            speech_to_text.load_backend("faster-whisper", "base")

    def test_unknown_backend_name_is_rejected(self):

        with self.assertRaises(ValueError):
            speech_to_text.load_backend("nope", "base")


class _FakeModel:

    def __init__(self, size):
        self.size = size

    def transcribe(self, samples, **_kwargs):
        return {"text": " Open Notepad. "}


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
