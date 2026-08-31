"""Mouse control."""

import pyautogui


def click(button="left"):
    """Click the mouse. ``button`` is ``left``, ``right`` or ``double``."""

    if button == "double":
        pyautogui.doubleClick()
    else:
        pyautogui.click(button=button)

    print(f"🖱️ Clicked ({button}).")

    return True


def scroll(amount):
    """Scroll up for a positive amount, down for a negative one."""

    pyautogui.scroll(amount)

    print(f"🖱️ Scrolled {'up' if amount > 0 else 'down'}.")

    return True


def move_to(x, y):
    """Move the cursor to an absolute screen position."""

    pyautogui.moveTo(x, y)

    return True
