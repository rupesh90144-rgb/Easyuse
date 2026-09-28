__version__ = "1.0.0"

import secrets
import string
from pathlib import Path

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window


class ToolkitApp(App):

    def build(self):
        self.title = "Personal Toolkit"
        self.notes_file = None

        root = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(10)
        )

        title = Label(
            text="[b]MY PERSONAL TOOLKIT[/b]",
            markup=True,
            font_size="24sp",
            size_hint_y=None,
            height=dp(55)
        )
        root.add_widget(title)

        self.output = Label(
            text="Welcome! Choose a tool below.",
            size_hint_y=1
        )
        root.add_widget(self.output)

        self.entry = TextInput(
            hint_text="Enter numbers or a note",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size="18sp"
        )
        root.add_widget(self.entry)

        self.second = TextInput(
            hint_text="Second number (if needed)",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size="18sp"
        )
        root.add_widget(self.second)

        buttons = [
            ("Calculator", self.calculate),
            ("Password Generator", self.password),
            ("Even / Odd Checker", self.even_odd),
            ("Number Sign Checker", self.sign_check),
            ("Save Note", self.save_note),
            ("View Notes", self.view_notes),
            ("Clear Inputs", self.clear_inputs),
        ]

        for text, action in buttons:
            button = Button(
                text=text,
                size_hint_y=None,
                height=dp(48),
                font_size="16sp"
            )
            button.bind(on_release=action)
            root.add_widget(button)

        return root

    def show_result(self, message):
        self.output.text = str(message)

    def calculate(self, *_):
        try:
            a = float(self.entry.text)
            b = float(self.second.text)
            self.show_result(f"Result: {a + b}")
        except ValueError:
            self.show_result("Enter two valid numbers.")

    def password(self, *_):
        chars = string.ascii_letters + string.digits + "!@#$%&*"
        result = "".join(
            secrets.choice(chars) for _ in range(16)
        )
        self.show_result("Generated password:\n" + result)

    def even_odd(self, *_):
        try:
            number = int(self.entry.text)
            answer = "even" if number % 2 == 0 else "odd"
            self.show_result(f"{number} is {answer}.")
        except ValueError:
            self.show_result("Enter a whole number.")

    def sign_check(self, *_):
        try:
            number = float(self.entry.text)
            if number > 0:
                answer = "positive"
            elif number < 0:
                answer = "negative"
            else:
                answer = "zero"
            self.show_result(f"{number} is {answer}.")
        except ValueError:
            self.show_result("Enter a valid number.")

    def save_note(self, *_):
        note = self.entry.text.strip()
        if not note:
            self.show_result("Type a note first.")
            return

        path = Path(self.user_data_dir) / "my_notes.txt"
        with path.open("a", encoding="utf-8") as f:
            f.write(note + "\n")

        self.show_result("Note saved!")
        self.entry.text = ""

    def view_notes(self, *_):
        path = Path(self.user_data_dir) / "my_notes.txt"
        if path.exists():
            notes = path.read_text(encoding="utf-8")
            self.show_result(notes or "No notes yet.")
        else:
            self.show_result("No notes saved yet.")

    def clear_inputs(self, *_):
        self.entry.text = ""
        self.second.text = ""
        self.show_result("Inputs cleared.")


if __name__ == "__main__":
    ToolkitApp().run()
