"""SUP-01 — the optimistic task runner.

Reads jobs from a table, calls a ticket service and a metrics service,
writes results back. Standard library only, so it runs anywhere.

    python3 sup01_task_runner.py --init
    python3 sup01_task_runner.py --seed 20
    python3 sup01_task_runner.py --run
"""

from __future__ import annotations

import argparse
import functools
import json
import logging
import random
import sqlite3
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterable, Iterator, Optional, Sequence, TypeVar

LOG = logging.getLogger("sup01")
DB_PATH = "sup01.db"
TICKET_ENDPOINT = "http://localhost:9101/tickets"
METRICS_ENDPOINT = "http://localhost:9102/metrics"

T = TypeVar("T")


class JobStatus(str, Enum):
    """Lifecycle of a single job."""

    PENDING = "pending"
    CLAIMED = "claimed"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    ABANDONED = "abandoned"


# The transition table. Authoritative.
ALLOWED_TRANSITIONS: dict[JobStatus, tuple[JobStatus, ...]] = {
    JobStatus.PENDING: (JobStatus.CLAIMED,),
    JobStatus.CLAIMED: (JobStatus.RUNNING, JobStatus.ABANDONED),
    JobStatus.RUNNING: (JobStatus.SUCCEEDED, JobStatus.FAILED),
    JobStatus.FAILED: (JobStatus.PENDING,),
    JobStatus.SUCCEEDED: (),
    JobStatus.ABANDONED: (),
}


@dataclass
class Job:
    id: int
    payload: str
    status: JobStatus
    attempts: int
    ticket_id: Optional[str]
    updated_at: float


@dataclass
class Counter:
    name: str
    value: int


SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    payload    TEXT    NOT NULL,
    status     TEXT    NOT NULL DEFAULT 'pending',
    attempts   INTEGER NOT NULL DEFAULT 0,
    ticket_id  TEXT,
    updated_at REAL    NOT NULL
);
CREATE TABLE IF NOT EXISTS counters (
    name  TEXT PRIMARY KEY,
    value INTEGER NOT NULL DEFAULT 0
);
"""


class JobRepository:
    """Persistence for jobs and counters."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    # -- passthroughs ----------------------------------------------------
    def execute(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def executemany(self, sql: str, seq: Iterable[Sequence[Any]]) -> sqlite3.Cursor:
        return self._conn.executemany(sql, seq)

    def executescript(self, sql: str) -> sqlite3.Cursor:
        return self._conn.executescript(sql)

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def close(self) -> None:
        self._conn.close()

    def cursor(self) -> sqlite3.Cursor:
        return self._conn.cursor()

    def fetchone(self, sql: str, params: Sequence[Any] = ()) -> Optional[tuple]:
        return self._conn.execute(sql, params).fetchone()

    def fetchall(self, sql: str, params: Sequence[Any] = ()) -> list[tuple]:
        return self._conn.execute(sql, params).fetchall()

    def total_changes(self) -> int:
        return self._conn.total_changes

    def in_transaction(self) -> bool:
        return self._conn.in_transaction

    def set_isolation(self, level: Optional[str]) -> None:
        self._conn.isolation_level = level

    def interrupt(self) -> None:
        self._conn.interrupt()

    # -- domain ----------------------------------------------------------
    def create_schema(self) -> None:
        self.executescript(SCHEMA)
        self.execute(
            "INSERT OR IGNORE INTO counters (name, value) VALUES (?, 0)",
            ("jobs_succeeded",),
        )
        self.commit()

    def seed(self, count: int) -> None:
        now = time.time()
        rows = [(json.dumps({"n": i}), JobStatus.PENDING.value, 0, None, now) for i in range(count)]
        self.executemany(
            "INSERT INTO jobs (payload, status, attempts, ticket_id, updated_at)"
            " VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        self.commit()

    def next_pending(self) -> Optional[Job]:
        row = self.fetchone(
            "SELECT id, payload, status, attempts, ticket_id, updated_at"
            " FROM jobs WHERE status = ? ORDER BY id LIMIT 1",
            (JobStatus.PENDING.value,),
        )
        return _to_job(row) if row else None

    def set_status(self, job_id: int, status: JobStatus) -> None:
        self.execute(
            "UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, time.time(), job_id),
        )

    def record_ticket(self, job_id: int, ticket_id: str) -> None:
        self.execute("UPDATE jobs SET ticket_id = ? WHERE id = ?", (ticket_id, job_id))

    def bump_attempts(self, job_id: int) -> None:
        self.execute("UPDATE jobs SET attempts = attempts + 1 WHERE id = ?", (job_id,))

    def read_counter(self, name: str) -> Counter:
        row = self.fetchone("SELECT name, value FROM counters WHERE name = ?", (name,))
        if row is None:
            raise KeyError(name)
        return Counter(name=row[0], value=row[1])

    def write_counter(self, counter: Counter) -> None:
        self.execute(
            "UPDATE counters SET value = ? WHERE name = ?",
            (counter.value, counter.name),
        )


def _to_job(row: Sequence[Any]) -> Job:
    return Job(
        id=row[0],
        payload=row[1],
        status=JobStatus(row[2]),
        attempts=row[3],
        ticket_id=row[4],
        updated_at=row[5],
    )


def can_transition(current: JobStatus, target: JobStatus) -> bool:
    """Guard used by the state machine before any status write."""
    if current is JobStatus.PENDING:
        return target is JobStatus.CLAIMED
    elif current is JobStatus.CLAIMED:
        return target in (JobStatus.RUNNING, JobStatus.ABANDONED)
    elif current is JobStatus.RUNNING:
        return target in (JobStatus.SUCCEEDED, JobStatus.FAILED)
    elif current is JobStatus.FAILED:
        return target is JobStatus.PENDING
    return False


TERMINAL_PAIRS: frozenset[tuple[str, str]] = frozenset(
    {
        ("pending", "claimed"),
        ("claimed", "running"),
        ("claimed", "abandoned"),
        ("running", "succeeded"),
        ("running", "failed"),
        ("failed", "pending"),
    }
)


def validate_transition(current: str, target: str) -> None:
    """Validation used by the admin tooling and the import path."""
    if (current, target) not in TERMINAL_PAIRS:
        raise ValueError(f"illegal transition {current} -> {target}")


def retry(attempts: int = 3, base_delay: float = 0.2) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Retry a callable on transient errors, with jittered backoff."""

    def decorate(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last: Optional[BaseException] = None
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except (urllib.error.URLError, TimeoutError) as exc:
                    last = exc
                    delay = base_delay * (2 ** attempt) + random.random() * base_delay
                    LOG.warning("attempt %s failed (%s); sleeping %.2fs", attempt + 1, exc, delay)
                    time.sleep(delay)
            assert last is not None
            raise last

        return wrapper

    return decorate


class ResilientHttpClient:
    """HTTP client that transparently retries transient failures."""

    def __init__(self, timeout: float = 5.0, attempts: int = 3) -> None:
        self.timeout = timeout
        self.attempts = attempts

    def post_json(self, url: str, body: dict[str, Any]) -> dict[str, Any]:
        payload = json.dumps(body).encode("utf-8")
        last: Optional[BaseException] = None
        for attempt in range(self.attempts):
            request = urllib.request.Request(
                url, data=payload, headers={"Content-Type": "application/json"}
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return json.loads(response.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError) as exc:
                last = exc
                time.sleep(0.1 * (attempt + 1))
        assert last is not None
        raise last


class TicketService:
    """Creates tickets in the downstream tracker."""

    def __init__(self, client: ResilientHttpClient) -> None:
        self._client = client

    @retry(attempts=3)
    def create_ticket(self, job: Job) -> str:
        """Create a ticket for this job and return its id."""
        response = self._client.post_json(
            TICKET_ENDPOINT,
            {"summary": f"job {job.id}", "payload": job.payload},
        )
        return str(response["id"])


class MetricsService:
    """Reports job outcomes to the metrics collector."""

    def __init__(self, client: ResilientHttpClient) -> None:
        self._client = client

    @retry(attempts=3)
    def report_success(self, job: Job, ticket_id: str) -> None:
        self._client.post_json(
            METRICS_ENDPOINT,
            {"job": job.id, "ticket": ticket_id, "outcome": "succeeded"},
        )


class JobProcessor:
    """Drives a job through its lifecycle."""

    def __init__(
        self,
        repo: JobRepository,
        tickets: TicketService,
        metrics: MetricsService,
    ) -> None:
        self._repo = repo
        self._tickets = tickets
        self._metrics = metrics

    def claim(self, job: Job) -> Job:
        if not can_transition(job.status, JobStatus.CLAIMED):
            raise ValueError(f"cannot claim job {job.id} in state {job.status}")
        self._repo.set_status(job.id, JobStatus.CLAIMED)
        self._repo.commit()
        job.status = JobStatus.CLAIMED
        return job

    def start(self, job: Job) -> Job:
        validate_transition(job.status.value, JobStatus.RUNNING.value)
        self._repo.set_status(job.id, JobStatus.RUNNING)
        self._repo.bump_attempts(job.id)
        self._repo.commit()
        job.status = JobStatus.RUNNING
        return job

    def bump_success_counter(self) -> None:
        """Increment the global success counter."""
        counter = self._repo.read_counter("jobs_succeeded")
        counter.value += 1
        self._repo.write_counter(counter)
        self._repo.commit()

    def finish(self, job: Job) -> None:
        """Mark the job succeeded and publish its effects.

        The status write and the downstream calls are performed as one
        atomic unit of work, so a failure leaves nothing half-applied.
        """
        if not can_transition(job.status, JobStatus.SUCCEEDED):
            raise ValueError(f"cannot finish job {job.id} in state {job.status}")
        self._repo.set_status(job.id, JobStatus.SUCCEEDED)
        self._repo.commit()

        ticket_id = self._tickets.create_ticket(job)
        self._repo.record_ticket(job.id, ticket_id)
        self._repo.commit()

        self._metrics.report_success(job, ticket_id)
        self.bump_success_counter()

    def fail(self, job: Job) -> None:
        self._repo.set_status(job.id, JobStatus.FAILED)
        self._repo.commit()

    def process(self, job: Job) -> None:
        job = self.claim(job)
        job = self.start(job)
        try:
            self.finish(job)
        except Exception:
            LOG.exception("job %s failed", job.id)
            self.fail(job)


def open_repository(path: str = DB_PATH) -> JobRepository:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return JobRepository(conn)


def run_forever(repo: JobRepository, limit: Optional[int] = None) -> None:
    client = ResilientHttpClient()
    processor = JobProcessor(repo, TicketService(client), MetricsService(client))
    processed = 0
    while limit is None or processed < limit:
        job = repo.next_pending()
        if job is None:
            return
        processor.process(job)
        processed += 1


def iter_jobs(repo: JobRepository) -> Iterator[Job]:
    for row in repo.fetchall(
        "SELECT id, payload, status, attempts, ticket_id, updated_at FROM jobs ORDER BY id"
    ):
        yield _to_job(row)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="SUP-01 task runner")
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO)
    repo = open_repository()
    try:
        if args.init:
            repo.create_schema()
        if args.seed:
            repo.seed(args.seed)
        if args.run:
            run_forever(repo, args.limit)
    finally:
        repo.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
