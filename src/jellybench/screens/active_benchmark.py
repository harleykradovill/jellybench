from ..ascii import LOGO
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Select, Static


class ActiveBenchmarkScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            Label("Running Benchmark..."),
            Label("Scenario: xxx"),
            Label("Runtime: xx:xx / xx:xx"),
            Label("Users Connected: 0/0"),
            Label("Requests"),
            Label("0"),
            Label("Throughput"),
            Label("0 req/sec"),
            Label("Latency"),
            Label("P50  0ms"),
            Label("P95  0ms"),
            Label("P99  0ms"),
            Label("Errors: 0"),
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
