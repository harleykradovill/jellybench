from datetime import datetime

from sqlalchemy import JSON, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

DB_URL = "sqlite:///jellybench.db"


class Base(DeclarativeBase):
    pass


class Benchmark(Base):
    __tablename__ = "benchmarks"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario: Mapped[str] = mapped_column(String)
    duration: Mapped[float] = mapped_column(Float)
    workers: Mapped[int] = mapped_column(Integer)
    results: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


_engine = create_engine(DB_URL)
Base.metadata.create_all(_engine)


def save_benchmark(scenario: str, duration: float, workers: int, results: dict) -> None:
    """
    Persist a completed benchmark run.

    :param scenario: Name of the benchmark scenario.
    :param duration: Benchmark duration in seconds.
    :param workers: Number of concurrent workers.
    :param results: Metrics snapshot to store as JSON.
    """
    with Session(_engine) as session:
        session.add(
            Benchmark(
                scenario=scenario,
                duration=duration,
                workers=workers,
                results=results,
            )
        )
        session.commit()
