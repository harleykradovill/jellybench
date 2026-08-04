from textual.app import App
from .screens.menu import MainMenu


class JellyBenchApp(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.push_screen(MainMenu())


if __name__ == "__main__":
    JellyBenchApp().run()
