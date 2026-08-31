import os
import subprocess
import webbrowser
import time

import pyautogui
import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel


# ==========================================
# SETTINGS
# ==========================================

MICROPHONE_DEVICE = 1
SAMPLE_RATE = 16000
RECORDING_DURATION = 5


# ==========================================
# LOAD WHISPER
# ==========================================

print("🧠 Loading voice recognition...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("✅ Voice recognition ready.")


# ==========================================
# APPLICATIONS
# ==========================================

APPLICATIONS = {
    "chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ],

    "google chrome": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ],

    "notepad": ["notepad.exe"],

    "calculator": ["calc.exe"]
}


# ==========================================
# OPEN APPLICATION
# ==========================================

def open_application(app):

    app = app.lower().strip()

    if app not in APPLICATIONS:
        print(f"❌ I don't know how to open {app}.")
        return

    paths = APPLICATIONS[app]

    for path in paths:

        if path.endswith(".exe"):

            if os.path.exists(path):
                subprocess.Popen([path])
                print(f"✅ Opening {app}.")
                return

        else:

            subprocess.Popen([path])
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
# PROCESS COMMAND
# ==========================================

def process_command(text):

    # Normalize capitalization
    command = text.lower().strip()

    print()
    print(f"🧠 Command: {command}")

    # --------------------------------------
    # OPEN APPLICATION
    # --------------------------------------

    if command.startswith("open "):

        app = command.replace("open ", "", 1).strip()

        open_application(app)

    # --------------------------------------
    # LAUNCH APPLICATION
    # --------------------------------------

    elif command.startswith("launch "):

        app = command.replace("launch ", "", 1).strip()

        open_application(app)

    # --------------------------------------
    # START APPLICATION
    # --------------------------------------

    elif command.startswith("start "):

        app = command.replace("start ", "", 1).strip()

        open_application(app)

    # --------------------------------------
    # TYPE
    # --------------------------------------

    elif command.startswith("type "):

        text_to_type = command.replace("type ", "", 1).strip()

        type_text(text_to_type)

    # --------------------------------------
    # ENTER
    # --------------------------------------

    elif command in ["enter", "press enter", "hit enter"]:

        press_key("enter")

    # --------------------------------------
    # SPACE
    # --------------------------------------

    elif command in ["space", "press space", "hit space"]:

        press_key("space")

    # --------------------------------------
    # BACKSPACE
    # --------------------------------------

    elif command in ["backspace", "press backspace"]:

        press_key("backspace")

    # --------------------------------------
    # TAB
    # --------------------------------------

    elif command in ["tab", "press tab"]:

        press_key("tab")

    # --------------------------------------
    # ESCAPE
    # --------------------------------------

    elif command in ["escape", "esc", "press escape"]:

        press_key("esc")

    # --------------------------------------
    # GO TO GOOGLE
    # --------------------------------------

    elif command in [
        "go to google",
        "open google",
        "visit google"
    ]:

        open_website("https://www.google.com")

    # --------------------------------------
    # GO TO YOUTUBE
    # --------------------------------------

    elif command in [
        "go to youtube",
        "open youtube",
        "visit youtube"
    ]:

        open_website("https://www.youtube.com")

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
    # EXIT
    # --------------------------------------

    elif command in [
        "exit",
        "quit",
        "stop",
        "goodbye"
    ]:

        return False

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

    recording = sd.rec(
        int(RECORDING_DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=MICROPHONE_DEVICE
    )

    sd.wait()

    write(
        "command.wav",
        SAMPLE_RATE,
        recording
    )

    print("🧠 Understanding...")

    segments, info = model.transcribe(
        "command.wav",
        beam_size=5
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    print()
    print("===================================")
    print("🎙️  VOICE AI")
    print("===================================")
    print("Speak a command...")
    print("Say 'exit' to stop.")

    command = listen()

    print()
    print("You said:")
    print(command)

    if not command:
        print("❌ I didn't hear anything.")
        continue

    should_continue = process_command(command)

    if not should_continue:
        print("👋 Voice AI shutting down.")
        break