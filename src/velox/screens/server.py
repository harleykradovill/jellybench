import asyncio

import httpx
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Label, Static, Button

from ..ascii import LOGO
from .error import ErrorScreen


def _field(response: httpx.Response, *keys: str, default: str = "Unknown") -> str:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        return f"HTTP {exc.response.status_code}"
    data = response.json()
    for key in keys:
        value = data.get(key)
        if value is not None:
            return str(value)
    return default


class ServerInformation(Screen):
    BINDINGS = [("f5", "refresh", "Refresh")]

    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            Label("Server Name", classes="info-label"),
            Label("Loading...", id="server-name", classes="info-value"),
            Label("Address", classes="info-label"),
            Label(self.app.config.server.url, id="address", classes="info-value"),
            Label("Status", classes="info-label"),
            Label("...", id="status", classes="info-value"),
            Label("Jellyfin Version", classes="info-label"),
            Label("...", id="version", classes="info-value"),
            Label("Movies", classes="info-sub"),
            Label("...", id="movies", classes="info-value"),
            Label("TV Shows", classes="info-sub"),
            Label("...", id="shows", classes="info-value"),
            Label("Users", classes="info-sub"),
            Label("...", id="users", classes="info-value"),
            Button("Go Back", id="return", classes="btn"),
            id="server-container",
        )
        yield Static("F5 - Refresh", classes="footer")

    def on_mount(self) -> None:
        self.action_refresh()

    def action_refresh(self) -> None:
        self.run_worker(self.load(), exclusive=True)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "return":
            self.app.pop_screen()

    async def load(self) -> None:
        url = self.app.config.server.url.rstrip("/")
        headers = {
            "Authorization": f'MediaBrowser Token="{self.app.config.server.api_key}"'
        }
        try:
            async with httpx.AsyncClient(
                base_url=url, headers=headers, timeout=10
            ) as client:
                info, counts, users = await asyncio.gather(
                    client.get("/System/Info"),
                    client.get("/Items/Counts"),
                    client.get("/Users/Public"),
                )
        except httpx.HTTPError:
            self.query_one("#status", Label).update("● Offline")
            return
        except Exception as error:
            ErrorScreen.show(
                self.app,
                "Server Information Failed",
                "Velox could not load the server information.",
                str(error),
            )
            return

        if any(response.status_code == 401 for response in (info, counts, users)):
            ErrorScreen.show(
                self.app,
                "Unauthorized",
                "Velox could not authenticate with the server.",
                "Check the API key in the configuration and try again.",
            )
            return

        self.query_one("#status", Label).update("● Online")
        self.query_one("#server-name", Label).update(
            _field(info, "serverName", "ServerName")
        )
        self.query_one("#version", Label).update(_field(info, "version", "Version"))
        self.query_one("#movies", Label).update(
            _field(counts, "movieCount", "MovieCount", default="0")
        )
        self.query_one("#shows", Label).update(
            _field(counts, "seriesCount", "SeriesCount", default="0")
        )
        self.query_one("#users", Label).update(self._user_count(users))

    def _user_count(self, response: httpx.Response) -> str:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            return f"HTTP {exc.response.status_code}"
        return str(len(response.json()))
