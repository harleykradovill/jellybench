class Metrics:
    def __init__(self) -> None:
        self._latencies: list[float] = []
        self._errors = 0

    def record(self, latency_ms: float, ok: bool) -> None:
        self._latencies.append(latency_ms)
        if not ok:
            self._errors += 1

    def snapshot(self) -> dict:
        lat = sorted(self._latencies)
        return {
            "requests": len(lat),
            "errors": self._errors,
            "p50": self._percentile(lat, 50),
            "p95": self._percentile(lat, 95),
            "p99": self._percentile(lat, 99),
        }

    @staticmethod
    def _percentile(sorted_lat: list[float], p: int) -> float:
        if not sorted_lat:
            return 0.0
        idx = min(len(sorted_lat) - 1, round(p / 100 * (len(sorted_lat) - 1)))
        return sorted_lat[idx]
