"""Keyboard control."""

import pyautogui


TYPING_INTERVAL = 0.03


def type_text(text):
    """Type text at the current cursor position."""

    pyautogui.write(text, interval=TYPING_INTERVAL)

    print("⌨️ Text typed.")

    return True


def press_key(key):
    """Press a single key, e.g. ``enter`` or ``esc``."""

    pyautogui.press(key)

    print(f"⌨️ Pressed {key}.")

    return True


def hotkey(*keys):
    """Press a key combination, e.g. ``hotkey("ctrl", "s")``."""

    pyautogui.hotkey(*keys)

    print(f"⌨️ Pressed {'+'.join(keys)}.")

    return True
