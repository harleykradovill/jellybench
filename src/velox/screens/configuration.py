from ..ascii import LOGO
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Input, Button, Label, Static


class ConfigurationScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            Label("Server URL"),
            Input(self.app.config.server.url, id="url", classes="input"),
            Label("API Key"),
            Input(
                self.app.config.server.api_key,
                id="api_key",
                password=True,
                classes="input",
            ),
            Button("Save", id="save", classes="btn"),
            Button("Go Back", id="return", classes="btn"),
            id="config-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.save()
        elif event.button.id == "return":
            self.app.pop_screen()

    def key_enter(self) -> None:
        self.save()

    def key_down(self) -> None:
        self.focus_next()

    def key_up(self) -> None:
        self.focus_previous()

    def save(self) -> None:
        self.app.config.server.url = self.query_one("#url", Input).value
        self.app.config.server.api_key = self.query_one("#api_key", Input).value
        self.app.config.save()
        self.app.pop_screen()
