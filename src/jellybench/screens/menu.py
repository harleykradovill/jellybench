from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label, Static
from textual import on
from ..ascii import LOGO

from .configuration import ConfigurationScreen
from .server import ServerInformation


class MainMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            ListView(
                ListItem(Label("Run Benchmark"), id="benchmark"),
                ListItem(Label("Server Information"), id="server"),
                ListItem(Label("Benchmark History"), id="history"),
                ListItem(Label("Compare Results"), id="compare"),
                ListItem(Label("Configuration"), id="configuration"),
                classes="optionslist",
            ),
            id="menu-container",
        )

    @on(ListView.Selected)
    def on_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "configuration":
            self.app.push_screen(ConfigurationScreen())
        elif event.item.id == "server":
            self.app.push_screen(ServerInformation())
