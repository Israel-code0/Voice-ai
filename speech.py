import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import time


# Microphone device
MICROPHONE_DEVICE = 1

# Whisper model
print("Loading speech recognition model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("✅ Speech recognition ready.")

# Recording settings
duration = 5
sample_rate = 16000

print()
print("🎙️ Get ready...")
time.sleep(2)

print("🎙️ Listening...")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16",
    device=MICROPHONE_DEVICE
)

sd.wait()

write(
    "test_recording.wav",
    sample_rate,
    recording
)

print("✅ Recording finished.")
print("🧠 Understanding what you said...")

segments, info = model.transcribe(
    "test_recording.wav",
    beam_size=5
)

text = ""

for segment in segments:
    text += segment.text

print()
print("You said:")
print(text.strip())