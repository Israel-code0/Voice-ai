"""Central configuration for Voice AI.

Everything here can be overridden with environment variables so the same code
runs on machines with different microphones and Chrome installs.
"""

import os

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv is only needed by the OpenAI scripts
    def load_dotenv():
        return False

load_dotenv()


def _device_from_env():
    """Return the configured input device, or None for the system default."""

    device = os.getenv("VOICE_AI_MIC_DEVICE")

    if not device:
        return None

    return int(device) if device.isdigit() else device


# ==========================================
# AUDIO
# ==========================================

MICROPHONE_DEVICE = _device_from_env()
SAMPLE_RATE = 16000
RECORDING_DURATION = int(os.getenv("VOICE_AI_RECORDING_DURATION", "5"))
RECORDING_FILE = os.getenv("VOICE_AI_RECORDING_FILE", "command.wav")


# ==========================================
# SPEECH TO TEXT
# ==========================================

# "auto", "faster-whisper", "whisper" (openai-whisper) or "openai" (API).
STT_BACKEND = os.getenv("VOICE_AI_STT_BACKEND", "auto")

OPENAI_TRANSCRIBE_MODEL = os.getenv(
    "VOICE_AI_OPENAI_TRANSCRIBE_MODEL", "whisper-1"
)

WHISPER_MODEL = os.getenv("VOICE_AI_WHISPER_MODEL", "base")
WHISPER_DEVICE = os.getenv("VOICE_AI_WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.getenv("VOICE_AI_WHISPER_COMPUTE_TYPE", "int8")


# ==========================================
# TEXT TO SPEECH
# ==========================================

SPEECH_ENABLED = os.getenv("VOICE_AI_SPEECH", "1") not in ("0", "false", "False")
SPEECH_RATE = int(os.getenv("VOICE_AI_SPEECH_RATE", "175"))


# ==========================================
# APPLICATIONS
# ==========================================

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(
        r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    ),
    "chrome.exe"
]

APPLICATIONS = {
    "chrome": CHROME_PATHS,
    "google chrome": CHROME_PATHS,
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "explorer": ["explorer.exe"],
    "file explorer": ["explorer.exe"],
    "paint": ["mspaint.exe"],
    "command prompt": ["cmd.exe"],
    "terminal": ["wt.exe", "cmd.exe"],
    "settings": ["ms-settings:"],
    "task manager": ["taskmgr.exe"]
}


# ==========================================
# WEBSITES
# ==========================================

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com",
    "wikipedia": "https://www.wikipedia.org"
}
