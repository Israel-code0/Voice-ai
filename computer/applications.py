"""Launching Windows applications and websites."""

import os
import shutil
import subprocess
import webbrowser

import config


def resolve_executable(path):
    """Return a launchable path, or None if the executable was not found.

    Absolute paths are checked on disk; bare names such as ``notepad.exe`` are
    looked up on PATH, and shell protocols such as ``ms-settings:`` are passed
    through untouched.
    """

    if os.path.isabs(path):
        return path if os.path.exists(path) else None

    if path.endswith(":"):
        return path

    return shutil.which(path)


def open_application(app):
    """Open a known application. Returns True when it was started."""

    app = app.lower().strip()

    if app not in config.APPLICATIONS:
        print(f"❌ I don't know how to open {app}.")
        return False

    for path in config.APPLICATIONS[app]:

        executable = resolve_executable(path)

        if executable is None:
            continue

        try:
            if executable.endswith(":"):
                os.startfile(executable)
            else:
                subprocess.Popen([executable])
        except OSError as error:
            print(f"❌ Could not start {app}: {error}")
            return False

        print(f"✅ Opening {app}.")
        return True

    print(f"❌ Could not find {app}.")
    return False


def open_website(url):
    """Open a URL in the default browser."""

    webbrowser.open(url)

    print(f"🌐 Opening {url}.")

    return True
