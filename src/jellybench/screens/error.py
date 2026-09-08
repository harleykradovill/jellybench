from textual.app import App, ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from ..ascii import LOGO


class ErrorScreen(Screen):
    """
    Full-screen error shown when something goes wrong.

    :param title: Title for the error
    :param message: Description of what went wrong
    :param detail: Optional raw error detail
    """

    def __init__(self, title: str, message: str, detail: str = "") -> None:
        super().__init__()
        self._title = title
        self._message = message
        self._detail = detail

    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            Label(self._title, id="error-title"),
            Label(self._message, id="error-message"),
            Label(self._detail, id="error-detail") if self._detail else None,
            Button("Go Back", id="return", classes="btn"),
            id="error-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "return":
            self.app.pop_screen()

    def key_escape(self) -> None:
        self.app.pop_screen()

    @staticmethod
    def show(app: App, title: str, message: str, detail: str = "") -> None:
        """
        Push an error screen onto the given app.

        :param app: The Textual app instance
        :param title: Title for the error
        :param message: Description of what went wrong
        :param detail: Optional raw error detail
        """
        app.push_screen(ErrorScreen(title, message, detail))
