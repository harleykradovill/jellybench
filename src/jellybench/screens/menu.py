from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import ListView, ListItem, Label, Static
from ..ascii import LOGO


class MainMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            ListView(
                ListItem(Label("Server Information"), id="server"),
                ListItem(Label("Run Benchmark"), id="benchmark"),
                ListItem(Label("Benchmark History"), id="history"),
                ListItem(Label("Compare Results"), id="compare"),
                ListItem(Label("Settings"), id="settings"),
                classes="optionslist",
            ),
            id="menu-container",
        )
