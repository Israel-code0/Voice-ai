import os
import time

import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


# None means "use the system default input device".
_device = os.getenv("VOICE_AI_MIC_DEVICE")
MICROPHONE_DEVICE = int(_device) if _device and _device.isdigit() else _device

DURATION = 5
SAMPLE_RATE = 16000
RECORDING_FILE = "test_recording.wav"


def main():

    print("Loading speech recognition model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("✅ Speech recognition ready.")

    print()
    print("🎙️ Get ready...")
    time.sleep(2)

    print("🎙️ Listening...")

    try:

        recording = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            device=MICROPHONE_DEVICE
        )

        sd.wait()

    except sd.PortAudioError as error:

        print(f"❌ Microphone error: {error}")
        print("Set VOICE_AI_MIC_DEVICE to a device index from:")
        print(sd.query_devices())

        return

    write(RECORDING_FILE, SAMPLE_RATE, recording)

    print("✅ Recording finished.")
    print("🧠 Understanding what you said...")

    segments, _info = model.transcribe(RECORDING_FILE, beam_size=5)

    text = "".join(segment.text for segment in segments)

    print()
    print("You said:")
    print(text.strip())


if __name__ == "__main__":
    main()
