"""Maps intents produced by the brain onto the functions that do the work.

Imports are done inside `build_tools` so `agent.brain` (and its tests) stay
free of the pyautogui / audio dependencies.
"""


def build_tools():
    """Return the action -> callable registry."""

    from computer import applications, keyboard, mouse

    return {
        "open_application": applications.open_application,
        "open_website": applications.open_website,
        "type_text": keyboard.type_text,
        "press_key": keyboard.press_key,
        "click": mouse.click,
        "scroll": mouse.scroll
    }


def execute(intent, tools=None):
    """Run an intent. Returns False when the assistant should stop."""

    if intent.action == "exit":
        return False

    if intent.action == "none":
        print("❌ I didn't hear anything.")
        return True

    if intent.action == "unknown":
        print("🤔 I don't understand that command yet.")
        return True

    tools = build_tools() if tools is None else tools

    tool = tools.get(intent.action)

    if tool is None:
        print(f"🤔 No tool for {intent.action}.")
        return True

    if intent.value is None:
        tool()
    else:
        tool(intent.value)

    return True
