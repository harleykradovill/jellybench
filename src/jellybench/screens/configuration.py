from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Input, Button, Label, Header, Footer


class ConfigurationScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Label("Server URL")
        yield Input(self.app.config.server.url, id="url")
        yield Label("API Key")
        yield Input(self.app.config.server.api_key, id="api_key", password=True)
        yield Button("Save", id="save")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            self.app.config.server.url = self.query_one("#url", Input).value
            self.app.config.server.api_key = self.query_one("#api_key", Input).value
            self.app.config.save()
            self.app.pop_screen()
