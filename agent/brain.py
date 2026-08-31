"""Turns transcribed speech into an intent.

This module is deliberately dependency free: it does not touch the microphone,
the screen or the OS, so the command grammar can be unit tested on its own.
"""

from dataclasses import dataclass

import config


PUNCTUATION = ".,!?;: "

APP_PREFIXES = ("open ", "launch ", "start ", "run ")
WEBSITE_PREFIXES = ("go to ", "visit ", "open ", "launch ", "start ")

EXIT_COMMANDS = ("exit", "quit", "stop", "goodbye", "shut down")

KEY_COMMANDS = {
    "enter": "enter",
    "press enter": "enter",
    "hit enter": "enter",
    "space": "space",
    "press space": "space",
    "hit space": "space",
    "backspace": "backspace",
    "press backspace": "backspace",
    "delete": "delete",
    "press delete": "delete",
    "tab": "tab",
    "press tab": "tab",
    "escape": "esc",
    "esc": "esc",
    "press escape": "esc"
}

CLICK_COMMANDS = {
    "click": "left",
    "click the mouse": "left",
    "left click": "left",
    "right click": "right",
    "double click": "double"
}


@dataclass(frozen=True)
class Intent:
    """A parsed command: an action name plus its argument."""

    action: str
    value: object = None


def normalize(text):
    """Lowercase and drop the punctuation Whisper adds to transcriptions."""

    return text.lower().strip().strip(PUNCTUATION)


def strip_prefix(command, prefixes):
    """Return the text after the first matching prefix, or None."""

    for prefix in prefixes:
        if command.startswith(prefix):
            return command[len(prefix):].strip()

    return None


def parse_command(text):
    """Parse transcribed text into an Intent."""

    command = normalize(text)
    # Keep the original casing so "type Hello World" types "Hello World".
    original = text.strip().strip(PUNCTUATION)

    if not command:
        return Intent("none")

    if command in EXIT_COMMANDS:
        return Intent("exit")

    target = strip_prefix(command, WEBSITE_PREFIXES)

    if target in config.WEBSITES:
        return Intent("open_website", config.WEBSITES[target])

    target = strip_prefix(command, APP_PREFIXES)

    if target:
        return Intent("open_application", target)

    if command.startswith(("type ", "write ")):
        return Intent("type_text", original.split(" ", 1)[1].strip())

    if command in KEY_COMMANDS:
        return Intent("press_key", KEY_COMMANDS[command])

    if command in CLICK_COMMANDS:
        return Intent("click", CLICK_COMMANDS[command])

    if "scroll down" in command:
        return Intent("scroll", -5)

    if "scroll up" in command:
        return Intent("scroll", 5)

    return Intent("unknown", command)
