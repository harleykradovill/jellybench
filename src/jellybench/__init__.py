from textual.app import App
from .config import Config
from .screens.menu import MainMenu


class JellyBenchApp(App):
    CSS_PATH = "style.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = Config.load()

    def on_mount(self) -> None:
        self.push_screen(MainMenu())


if __name__ == "__main__":
    JellyBenchApp().run()
