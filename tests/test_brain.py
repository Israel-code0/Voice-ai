"""Unit tests for the command grammar. No audio or GUI dependencies needed.

Run with: python -m unittest discover -s tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.brain import Intent, parse_command  # noqa: E402
from agent.tools import execute  # noqa: E402


class ParseCommandTests(unittest.TestCase):

    def assert_intent(self, text, action, value=None):
        self.assertEqual(parse_command(text), Intent(action, value))

    def test_websites_win_over_the_open_prefix(self):
        self.assert_intent("Open Google.", "open_website",
                           "https://www.google.com")
        self.assert_intent("go to youtube", "open_website",
                           "https://www.youtube.com")

    def test_applications(self):
        self.assert_intent("Open Notepad.", "open_application", "notepad")
        self.assert_intent("launch calculator", "open_application",
                           "calculator")

    def test_typing_keeps_capitalization(self):
        self.assert_intent("Type Hello World", "type_text", "Hello World")

    def test_trailing_punctuation_is_ignored(self):
        self.assert_intent("Press Enter.", "press_key", "enter")
        self.assert_intent("Click.", "click", "left")

    def test_scrolling(self):
        self.assert_intent("scroll down", "scroll", -5)
        self.assert_intent("scroll up", "scroll", 5)

    def test_exit_and_empty(self):
        self.assert_intent("Goodbye.", "exit")
        self.assert_intent("   ", "none")

    def test_unknown(self):
        self.assert_intent("make me a sandwich", "unknown",
                           "make me a sandwich")


class ExecuteTests(unittest.TestCase):

    def setUp(self):
        self.calls = []
        self.tools = {
            "open_application": lambda app: self.calls.append(("app", app)),
            "open_website": lambda url: self.calls.append(("web", url)),
            "type_text": lambda text: self.calls.append(("type", text)),
            "press_key": lambda key: self.calls.append(("key", key)),
            "click": lambda button: self.calls.append(("click", button)),
            "scroll": lambda amount: self.calls.append(("scroll", amount))
        }

    def run_command(self, text):
        return execute(parse_command(text), self.tools)

    def test_dispatches_to_the_matching_tool(self):
        self.assertTrue(self.run_command("Open Notepad."))
        self.assertTrue(self.run_command("Type Hello World"))

        self.assertEqual(
            self.calls,
            [("app", "notepad"), ("type", "Hello World")]
        )

    def test_exit_stops_the_loop(self):
        self.assertFalse(self.run_command("exit"))

    def test_unknown_command_is_ignored(self):
        self.assertTrue(self.run_command("make me a sandwich"))
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
