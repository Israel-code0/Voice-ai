import os
import shutil
import subprocess
import webbrowser

import pyautogui
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


# ==========================================
# SETTINGS
# ==========================================

# None means "use the system default input device".
_device = os.getenv("VOICE_AI_MIC_DEVICE")
MICROPHONE_DEVICE = int(_device) if _device and _device.isdigit() else _device

SAMPLE_RATE = 16000
RECORDING_DURATION = 5
RECORDING_FILE = "command.wav"

WHISPER_MODEL = os.getenv("VOICE_AI_WHISPER_MODEL", "base")


# ==========================================
# LOAD WHISPER
# ==========================================

_model = None


def get_model():

    global _model

    if _model is None:

        print("🧠 Loading voice recognition...")

        _model = WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )

        print("✅ Voice recognition ready.")

    return _model


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

    "file explorer": ["explorer.exe"]
}


WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com"
}


# ==========================================
# OPEN APPLICATION
# ==========================================

def resolve_executable(path):
    """Return a launchable path, or None if the executable was not found."""

    if os.path.isabs(path):
        return path if os.path.exists(path) else None

    return shutil.which(path)


def open_application(app):

    app = app.lower().strip()

    if app not in APPLICATIONS:
        print(f"❌ I don't know how to open {app}.")
        return

    for path in APPLICATIONS[app]:

        executable = resolve_executable(path)

        if executable is None:
            continue

        try:
            subprocess.Popen([executable])
        except OSError as error:
            print(f"❌ Could not start {app}: {error}")
            return

        print(f"✅ Opening {app}.")
        return

    print(f"❌ Could not find {app}.")


# ==========================================
# TYPE TEXT
# ==========================================

def type_text(text):

    pyautogui.write(text, interval=0.03)

    print("⌨️ Text typed.")


# ==========================================
# PRESS KEY
# ==========================================

def press_key(key):

    pyautogui.press(key)

    print(f"⌨️ Pressed {key}.")


# ==========================================
# OPEN WEBSITE
# ==========================================

def open_website(url):

    webbrowser.open(url)

    print(f"🌐 Opening {url}.")


# ==========================================
# NORMALIZE
# ==========================================

def normalize(text):
    """Lowercase and drop the punctuation Whisper adds to transcriptions."""

    return text.lower().strip().strip(".,!?;: ")


# ==========================================
# PROCESS COMMAND
# ==========================================

def process_command(text):

    command = normalize(text)

    # Keep the original casing so "type Hello World" types "Hello World".
    original = text.strip().strip(".,!?;: ")

    print()
    print(f"🧠 Command: {command}")

    # --------------------------------------
    # EXIT
    # --------------------------------------

    if command in ["exit", "quit", "stop", "goodbye"]:

        return False

    # --------------------------------------
    # WEBSITES
    # --------------------------------------

    website = None

    for prefix in ["go to ", "visit ", "open ", "launch ", "start "]:

        if command.startswith(prefix):

            website = WEBSITES.get(command[len(prefix):].strip())
            break

    if website is not None:

        open_website(website)

    # --------------------------------------
    # OPEN APPLICATION
    # --------------------------------------

    elif (
        command.startswith("open ")
        or command.startswith("launch ")
        or command.startswith("start ")
    ):

        app = command.split(" ", 1)[1].strip()

        open_application(app)

    # --------------------------------------
    # TYPE
    # --------------------------------------

    elif command.startswith("type "):

        type_text(original.split(" ", 1)[1].strip())

    # --------------------------------------
    # KEYS
    # --------------------------------------

    elif command in ["enter", "press enter", "hit enter"]:

        press_key("enter")

    elif command in ["space", "press space", "hit space"]:

        press_key("space")

    elif command in ["backspace", "press backspace"]:

        press_key("backspace")

    elif command in ["tab", "press tab"]:

        press_key("tab")

    elif command in ["escape", "esc", "press escape"]:

        press_key("esc")

    # --------------------------------------
    # CLICK
    # --------------------------------------

    elif command in ["click", "click the mouse"]:

        pyautogui.click()

        print("🖱️ Clicked.")

    # --------------------------------------
    # SCROLL
    # --------------------------------------

    elif "scroll down" in command:

        pyautogui.scroll(-5)

        print("🖱️ Scrolled down.")

    elif "scroll up" in command:

        pyautogui.scroll(5)

        print("🖱️ Scrolled up.")

    # --------------------------------------
    # UNKNOWN COMMAND
    # --------------------------------------

    else:

        print("🤔 I don't understand that command yet.")

    return True


# ==========================================
# LISTEN
# ==========================================

def listen():

    print()
    print("🎙️ Listening...")

    try:

        recording = sd.rec(
            int(RECORDING_DURATION * SAMPLE_RATE),
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

        return ""

    write(RECORDING_FILE, SAMPLE_RATE, recording)

    print("🧠 Understanding...")

    segments, _info = get_model().transcribe(RECORDING_FILE, beam_size=5)

    return "".join(segment.text for segment in segments).strip()


# ==========================================
# MAIN LOOP
# ==========================================

def main():

    get_model()

    while True:

        print()
        print("===================================")
        print("🎙️  VOICE AI")
        print("===================================")
        print("Speak a command...")
        print("Say 'exit' to stop.")

        try:
            command = listen()
        except KeyboardInterrupt:
            print()
            print("👋 Voice AI shutting down.")
            break

        print()
        print("You said:")
        print(command)

        if not command:
            print("❌ I didn't hear anything.")
            continue

        if not process_command(command):
            print("👋 Voice AI shutting down.")
            break


if __name__ == "__main__":
    main()
