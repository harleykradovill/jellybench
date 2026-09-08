import httpx
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from ..ascii import LOGO
from ..benchmark import BenchmarkRunner
from .benchmark_details import BenchmarkDetailsScreen
from .error import ErrorScreen


def _parse_duration(value: str) -> float:
    if value.endswith("m"):
        return int(value[:-1]) * 60
    return int(value[:-1])


def _fmt_ms(ms: float) -> str:
    return f"{ms:.0f}ms"


class ActiveBenchmarkScreen(Screen):
    def __init__(self, scenario, users: int, duration: str, config) -> None:
        super().__init__()
        self.runner = BenchmarkRunner(
            scenario=scenario,
            users=users,
            duration=_parse_duration(duration),
            config=config,
        )

    def compose(self) -> ComposeResult:
        yield Static(LOGO, id="logo")
        yield Container(
            Label("Running Benchmark..."),
            Label(f"Scenario: {self.runner.scenario.name}"),
            Label("Runtime: 00:00 / 00:00", id="runtime"),
            Label(f"Users Connected: 0/{self.runner.users}", id="users"),
            Label("Requests"),
            Label("0", id="requests"),
            Label("Throughput"),
            Label("0 req/sec", id="throughput"),
            Label("Latency"),
            Label("P50  0ms", id="p50"),
            Label("P95  0ms", id="p95"),
            Label("P99  0ms", id="p99"),
            Label("Errors: 0", id="errors"),
            Button("Cancel Benchmark", id="return", classes="btn"),
            id="run-container",
        )

    def on_mount(self) -> None:
        self.run_worker(self._run(), exclusive=True)
        self._timer = self.set_interval(1, self._refresh)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "return":
            self.runner.stop()
            self.app.pop_screen()

    def key_down(self) -> None:
        self.focus_next()

    def key_up(self) -> None:
        self.focus_previous()

    async def _run(self) -> None:
        try:
            await self.runner.run()
        except httpx.HTTPError as error:
            ErrorScreen.show(
                self.app,
                "Benchmark Failed",
                "Velox could not connect to the Jellyfin server.",
                str(error),
            )
        except Exception as error:
            ErrorScreen.show(
                self.app,
                "Unexpected Error",
                "An unexpected error occurred while running the benchmark.",
                str(error),
            )

    def _refresh(self) -> None:
        elapsed = self.runner.elapsed
        total = self.runner.duration
        snap = self.runner.metrics.snapshot()
        self.query_one("#runtime", Label).update(
            f"Runtime: {self._fmt_clock(elapsed)} / {self._fmt_clock(total)}"
        )
        self.query_one("#users", Label).update(
            f"Workers Connected: {self.runner.active_users}/{self.runner.users}"
        )
        self.query_one("#requests", Label).update(f"{snap['requests']:,}")
        self.query_one("#throughput", Label).update(
            f"{snap['requests'] / max(elapsed, 1):.0f} req/sec"
        )
        self.query_one("#p50", Label).update(f"P50  {_fmt_ms(snap['p50'])}")
        self.query_one("#p95", Label).update(f"P95  {_fmt_ms(snap['p95'])}")
        self.query_one("#p99", Label).update(f"P99  {_fmt_ms(snap['p99'])}")
        self.query_one("#errors", Label).update(f"Errors: {snap['errors']}")
        if self.runner.done:
            self._timer.stop()
            self.app.push_screen(BenchmarkDetailsScreen(self.runner.benchmark))

    @staticmethod
    def _fmt_clock(seconds: float) -> str:
        minutes, secs = divmod(int(seconds), 60)
        return f"{minutes:02d}:{secs:02d}"
