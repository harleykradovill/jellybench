from ..ascii import LOGO
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Select, Static

SCENARIOS = [
    ("Mixed User Simulation", "mixed"),
    ("Streaming Test", "streaming"),
    ("API Stress Test", "api"),
    ("Library Browsing", "library"),
    ("Metadata Test", "metadata"),
]

DURATIONS = [
    ("1 minute", "1m"),
    ("5 minutes", "5m"),
    ("10 minutes", "10m"),
    ("30 minutes", "30m"),
]


class RunBenchmarkScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            Label("Scenario"),
            Select(SCENARIOS, id="scenario", classes="select"),
            Label("Virtual Users"),
            Input("100", id="users", classes="input"),
            Label("Duration"),
            Select(DURATIONS, id="duration", classes="select"),
            Button("Start Benchmark", id="start", classes="btn"),
            Button("Go Back", id="return", classes="btn"),
            id="run-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "return":
            self.app.pop_screen()

    def key_down(self) -> None:
        self.focus_next()

    def key_up(self) -> None:
        self.focus_previous()
