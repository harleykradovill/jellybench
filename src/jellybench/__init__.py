from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static


class StartupScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("JellyBench", classes="title")
        yield Static("Hello world!", classes="subtitle")
        yield Footer()


class JellyBenchApp(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.push_screen(StartupScreen())


if __name__ == "__main__":
    JellyBenchApp().run()
