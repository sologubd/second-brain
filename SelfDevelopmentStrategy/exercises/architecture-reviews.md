# Architecture review exercises

## How to use these

Three reviews across the first twelve weeks, in two modes. Two are
**self-inspection** — you review what you built. One works on a **supplied
deliberately bad system**, because reviewing your own code only ever demonstrates
that you can describe your own choices favourably, and finding a defect somebody
else planted is the harder and more transferable skill.

Every review runs against the same fourteen defect classes below, and every
finding must cite evidence. A class marked absent needs the same justification as
a class marked present: a checklist ticked without evidence is a document, not a
review.

The instrument is a set of questions, not a set of names. Four of them recur
often enough that week 04 formalises them into a versioned checklist and week 12
widens them into a five-axis rubric. Asked of any function, they are: **repeat
it** — call it twice and say what differs; **interrupt it** — kill the process
between two adjacent statements and say what survives; **collide it** — run two
copies concurrently and say who wins; and **name its assumptions** — state what
this code believes about a system it does not control, that nothing in the file
records.

None of the four can be answered by reading for style, and that is the entire
point. Generated code is syntactically clean, idiomatic, well-named and
consistently formatted, so every signal a reviewer habitually leans on now
reports green. The defects moved; they did not disappear. They sit at repetition,
at crash windows, at concurrency and at unstated external contracts, which is
precisely where reading does not look and where these four questions do.

Rungs are named per exercise. The set is anchored at **explain** (`DL-8`), which
canon defines as writing the decision record, naming the defects you are
accepting, and defending your threshold to somebody who will push back — and the
supplied-system review adds **debug** (`DL-4`), because finding a planted defect
in clean code is the same skill as diagnosing a fault whose evidence lies.

### What a finding looks like

A finding has four parts and is worthless without any of them: the **class id**
it belongs to, the **location** it lives at, the **evidence** that it is real,
and the **consequence** if nobody fixes it. Evidence is ranked, and the ranking
matters more than it looks. A reproduction — a second call that produces a second
effect, an injected process death that loses one, two concurrent runs that
disagree — is the strongest and is the only kind that cannot be argued with. A
line-level citation with an argument is next. An impression is not evidence and
does not enter the record, however experienced the reviewer.

The same discipline applies to a class you mark **absent**. Absence has two very
different causes: the defect genuinely cannot occur because of something you
built, or the surface where it would appear does not exist yet. Those are not the
same claim, and a review that conflates them will report a system getting safer
when it is only staying small.

### The two modes fail differently

Self-inspection fails by *charity*. You know why every decision was made, so a
defect reads as a tradeoff and the review turns into a justification with
headings. The counter is the checklist: a question you must answer in writing has
no room for the reason you already believe.

The supplied-system review fails by *fluency*. The code reads well, so the
reviewer's confidence rises while their evidence does not, and the review
converges on style notes. The counter is the reproduction requirement: two of
your findings must survive being run, not merely being argued.

This is why both modes are in the programme rather than either. They are not two
difficulty levels of one exercise; they are two different failure modes of the
same reviewer, and each is invisible from inside the other.

Weekly hours and acceptance live in [weeks/](../weeks/week-08.md). The systems
under self-inspection are defined in
[the platform file](../projects/engineering-agent-platform.md). This file owns
the defect classes, the supplied systems and the review bodies.

## The fourteen defect classes

Each class carries a **detection question**, and the question is the usable part.
Several have shifted meaning under generated code, and where they have, the
shift is stated rather than assumed.

| Id | Class | Detection question |
|---|---|---|
| `DC-01` | unnecessary abstractions | Does this interface have exactly one implementation and no second one in prospect? Speculative generality used to be justified by "changing it later is expensive"; later is now cheap, so the rule of three got stronger, not weaker. |
| `DC-02` | accidental coupling | If I deleted this module and regenerated it from its contract alone, what would the regeneration get wrong? Every answer names a coupling the type system does not show. |
| `DC-03` | shallow modules | What is the ratio of public symbols to implementation size? A module whose interface is as large as its body has hidden nothing and buys nothing. |
| `DC-04` | wrong boundaries | Does a single behaviour change require edits in two modules? Then the boundary is misplaced however clean each side looks. |
| `DC-05` | primitive obsession | Is a domain concept carried as a bare `str` or `int`? This costs more than it used to: a frozen newtype carries semantics to an agent at the call site, and a bare string carries none. |
| `DC-06` | duplicated logic | Is the duplicated thing an implementation or a decision? Duplicated implementations are cheap now and often preferable. Duplicated decisions — a business rule, a key format, a transition table, a retry classification — are more dangerous than ever, because three copies get regenerated separately and drift silently. |
| `DC-07` | incorrect state modeling | Is there a state the code can reach that the transition table does not list? Is there a listed transition no code performs? Both are defects and only the first is usually looked for. |
| `DC-08` | non-idempotent operations | What happens on the second call? Ask it of every side-effecting function, because the test suite asked it of none. |
| `DC-09` | hidden distributed transactions | Does any path commit locally and then call an external system? That is a crash window, and no test that does not kill the process between those two statements will ever find it. |
| `DC-10` | race conditions | What happens if two of these run at once — specifically, is there a read-modify-write with no conditional update, version column or row lock? An agent writes read-modify-write by default, because it is the readable form. |
| `DC-11` | failure recovery problems | If the process holding this work dies, who notices and how? If the answer is a timeout, what distinguishes slow from dead, and what happens when that guess is wrong? |
| `DC-12` | unbounded retries | Is there an aggregate budget, or only per-layer counts? Three layers retrying three times each is twenty-seven calls to a service already failing — and under a flat-rate plan the failure mode is a silent stall, not an error. |
| `DC-13` | authorization leaks | Is the permission check applied before or after ranking, filtering or counting? Post-filtering leaks existence through result count, latency and ranking even when content is withheld, and a test asserting "no unauthorized content returned" passes anyway. |
| `DC-14` | excessive agent permissions | Does this agent hold the union of every permission any of its steps ever needed? Can a low-privilege step cause a high-privilege step to act without re-checking the original human request? |

## The two supplied systems

Both are supplied in full below, as source. A review exercise you cannot run,
instrument and break is a reading exercise, and reading is exactly the activity
these defects are designed to survive.

Both files depend on the standard library only, so neither needs an environment
built before the review can start. Save each block to a file of its own and run
it. `SUP-01` initialises its own store and seeds work with
`python3 sup01_task_runner.py --init --seed 5`; its `--run` path expects two
local HTTP services on the ports named at the top of the file, and standing up
two trivial stubs is itself part of the review, because what the runner does when
those stubs misbehave is the question. `SUP-02` needs nothing external at all:
`python3 sup02_knowledge_assistant.py --self-check` builds a two-tenant index in
memory, asks the same question as two different users, and prints the citations
and the result count for each. Record both numbers before forming any opinion.
They are data, and one of them is a finding.

A note on the shape of both systems. Neither contains a mistake that reads as a
mistake. There is no bare `except`, no commented-out block, no obviously wrong
name. Every defect in both files survives a careful read by someone who is
looking for defects, which is the property that took the longest to build into
them and the one that makes them worth the hours.

**`SUP-01` — the optimistic task runner.** Roughly four hundred lines of Python
that reads jobs from a table, calls two external services and writes results
back. It is idiomatic, fully type-annotated, well-named and would pass any
linter. It is broken in six of the fourteen ways: `DC-03`, `DC-06`, `DC-08`,
`DC-09`, `DC-10` and `DC-12`. **Do not read the list before the review** — it is
recorded here because a supplied system whose defects were never written down is
not gradeable, not because it is meant to be consulted first.

```python
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
```

**`SUP-02` — the helpful knowledge assistant.** Roughly three hundred lines
serving two tenants from one index: clean, readable, tested. It carries four
defects — `DC-01`, `DC-05`, `DC-13` and `DC-14` — and it is deliberately the same
shape as the learner's own retrieval agent, seen from the outside.

```python
"""SUP-02 — the helpful knowledge assistant.

Answers questions from an indexed corpus, serving two tenants from one
index. Standard library only; the embedding function is a stand-in.
"""

from __future__ import annotations

import json
import math
import os
import sqlite3
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Sequence

API_TOKEN = os.environ.get("ASSISTANT_API_TOKEN", "")
LLM_ENDPOINT = "http://localhost:9103/complete"
INDEX_PATH = "sup02.db"
DEFAULT_K = 10

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT NOT NULL,
    doc_id    TEXT NOT NULL,
    body      TEXT NOT NULL,
    embedding TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS chunks_tenant ON chunks (tenant_id);
"""


@dataclass(frozen=True)
class Chunk:
    id: int
    tenant_id: str
    doc_id: str
    body: str
    embedding: list[float]


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: float


def embed(text: str) -> list[float]:
    """Deterministic stand-in embedding: character-histogram, normalised."""
    vector = [0.0] * 32
    for character in text.lower():
        vector[ord(character) % 32] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def cosine(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


class RetrieverStrategy(ABC):
    """Pluggable retrieval backend."""

    @abstractmethod
    def search(self, query: str, k: int) -> list[ScoredChunk]:
        ...


class VectorRetriever(RetrieverStrategy):
    """Cosine similarity over the whole index."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def _all_chunks(self) -> list[Chunk]:
        rows = self._conn.execute(
            "SELECT id, tenant_id, doc_id, body, embedding FROM chunks"
        ).fetchall()
        return [
            Chunk(
                id=row[0],
                tenant_id=row[1],
                doc_id=row[2],
                body=row[3],
                embedding=json.loads(row[4]),
            )
            for row in rows
        ]

    def search(self, query: str, k: int) -> list[ScoredChunk]:
        query_vector = embed(query)
        scored = [
            ScoredChunk(chunk=chunk, score=cosine(query_vector, chunk.embedding))
            for chunk in self._all_chunks()
        ]
        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:k]


class PermissionService:
    """Decides whether a caller may see a chunk."""

    def __init__(self, memberships: dict[str, set[str]]) -> None:
        self._memberships = memberships

    def visible_tenants(self, user_id: str) -> set[str]:
        return self._memberships.get(user_id, set())

    def can_see(self, user_id: str, chunk: Chunk) -> bool:
        return chunk.tenant_id in self.visible_tenants(user_id)


class Ingestor:
    """Writes documents into the shared index."""

    def __init__(self, conn: sqlite3.Connection, token: str = API_TOKEN) -> None:
        self._conn = conn
        self._token = token

    def create_schema(self) -> None:
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def fetch_remote(self, url: str) -> str:
        request = urllib.request.Request(
            url, headers={"Authorization": f"Bearer {self._token}"}
        )
        with urllib.request.urlopen(request, timeout=10.0) as response:
            return response.read().decode("utf-8")

    def ingest(self, tenant_id: str, doc_id: str, body: str) -> int:
        chunks = [body[start : start + 400] for start in range(0, len(body), 400)]
        cursor = self._conn.cursor()
        for text in chunks:
            cursor.execute(
                "INSERT INTO chunks (tenant_id, doc_id, body, embedding)"
                " VALUES (?, ?, ?, ?)",
                (tenant_id, doc_id, text, json.dumps(embed(text))),
            )
        self._conn.commit()
        return len(chunks)


class LlmClient:
    """Calls the completion endpoint."""

    def __init__(self, token: str = API_TOKEN) -> None:
        self._token = token

    def complete(self, prompt: str) -> str:
        payload = json.dumps({"prompt": prompt}).encode("utf-8")
        request = urllib.request.Request(
            LLM_ENDPOINT,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._token}",
            },
        )
        with urllib.request.urlopen(request, timeout=30.0) as response:
            return json.loads(response.read().decode("utf-8"))["text"]


class Assistant:
    """Answers a question for a user, from the documents that user may see."""

    def __init__(
        self,
        retriever: RetrieverStrategy,
        permissions: PermissionService,
        llm: LlmClient,
    ) -> None:
        self._retriever = retriever
        self._permissions = permissions
        self._llm = llm

    def _authorized(self, user_id: str, results: Sequence[ScoredChunk]) -> list[ScoredChunk]:
        return [item for item in results if self._permissions.can_see(user_id, item.chunk)]

    def answer(self, user_id: str, question: str, k: int = DEFAULT_K) -> dict[str, Any]:
        results = self._retriever.search(question, k)
        visible = self._authorized(user_id, results)
        context = "\n\n".join(item.chunk.body for item in visible)
        prompt = (
            "Answer the question using only the context below.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}\n"
        )
        return {
            "answer": self._llm.complete(prompt),
            "citations": [item.chunk.doc_id for item in visible],
            "result_count": len(visible),
        }


def open_index(path: str = INDEX_PATH) -> sqlite3.Connection:
    return sqlite3.connect(path)


def build_assistant(
    conn: sqlite3.Connection, memberships: dict[str, set[str]]
) -> Assistant:
    return Assistant(
        retriever=VectorRetriever(conn),
        permissions=PermissionService(memberships),
        llm=LlmClient(),
    )


def demo(user_id: str, question: str) -> Optional[dict[str, Any]]:
    conn = open_index()
    try:
        assistant = build_assistant(conn, {"alice": {"tenant-a"}, "bob": {"tenant-b"}})
        return assistant.answer(user_id, question)
    finally:
        conn.close()


SAMPLE_DOCS: list[tuple[str, str, str]] = [
    ("tenant-a", "handbook-a", "Expense claims are approved by the team lead."),
    ("tenant-a", "policy-a", "Laptops are replaced every three years."),
    ("tenant-b", "handbook-b", "Expense claims are approved by finance."),
    ("tenant-b", "policy-b", "Laptops are replaced every four years."),
    ("tenant-b", "faq-b", "Expense claims over 500 need a second approver."),
    ("tenant-b", "notes-b", "Expense policy was revised last quarter."),
    ("tenant-b", "memo-b", "Expense claims must cite a project code."),
]


def seed_demo(conn: sqlite3.Connection) -> int:
    """Populate a two-tenant index skewed towards one tenant."""
    ingestor = Ingestor(conn)
    ingestor.create_schema()
    written = 0
    for tenant_id, doc_id, body in SAMPLE_DOCS:
        written += ingestor.ingest(tenant_id, doc_id, body * 12)
    return written


def tenant_counts(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute(
        "SELECT tenant_id, COUNT(*) FROM chunks GROUP BY tenant_id"
    ).fetchall()
    return {row[0]: row[1] for row in rows}


class StubLlm(LlmClient):
    """Offline stand-in so the service can be exercised without a server."""

    def __init__(self) -> None:
        super().__init__(token="stub")

    def complete(self, prompt: str) -> str:
        return f"stub answer over {len(prompt)} characters of context"


def self_check() -> None:
    """Smoke test: both tenants can ask, and neither sees the other's text."""
    conn = sqlite3.connect(":memory:")
    try:
        seed_demo(conn)
        memberships = {"alice": {"tenant-a"}, "bob": {"tenant-b"}}
        assistant = Assistant(
            retriever=VectorRetriever(conn),
            permissions=PermissionService(memberships),
            llm=StubLlm(),
        )
        for user_id, tenant_id in (("alice", "tenant-a"), ("bob", "tenant-b")):
            result = assistant.answer(user_id, "how are expense claims approved?")
            assert "answer" in result, "no answer produced"
            visible_docs = set(result["citations"])
            allowed = {
                doc_id for tid, doc_id, _ in SAMPLE_DOCS if tid == tenant_id
            }
            assert visible_docs <= allowed, f"{user_id} saw a foreign document"
            print(f"{user_id}: {result['result_count']} results, docs={sorted(visible_docs)}")
        print("tenant chunk counts:", tenant_counts(conn))
    finally:
        conn.close()


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="SUP-02 knowledge assistant")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--ask", nargs=2, metavar=("USER", "QUESTION"))
    args = parser.parse_args(argv)

    if args.self_check:
        self_check()
    if args.ask:
        print(json.dumps(demo(args.ask[0], args.ask[1]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## Exercises

### AR-01 — self-inspection of the platform through S2 (D-w04-3)

Rungs: `DL-8` explain.

#### Objective

Review your own platform at the moment it first opens pull requests, using the
checklist you wrote the same week, and find at least one defect your ordinary
instincts would not have surfaced.

#### Task

Write the versioned generated-code review checklist first, built around the four
recurring questions, then apply it to the platform through `S2` — including to
`S2`'s own diff. Work through the fourteen classes above, recording each as
present or absent with the evidence that decided it. Produce the result as an
architecture decision record.

#### Constraints

- The checklist is written before the review and versioned, so a later review can be compared against this one.
- A class marked absent carries evidence, exactly as a class marked present does.
- At least one finding must come from applying a question the checklist added, not from general impression.
- The review covers the platform's own code, not its dependencies.

#### Deliverable

`D-w04-3` — an **ADR** (`DT-04`) recording the review, delivered alongside
version 1 of the review checklist.

#### Acceptance criteria

- The checklist is versioned and carries at least 4 question categories.
- The ADR names at least 3 of the 14 defect classes as present or absent, each with cited evidence rather than a tick.
- Applying the checklist to the `S2` diff produced at least 1 recorded finding.
- 100% of findings name the defect-class id they belong to.

#### Metrics

- Success rate: defect classes assessed with evidence divided by 14.
- Failure rate: findings later reclassified as false positives divided by findings recorded, assessed at the next review.

#### Reflection questions

1. Which finding would your unaided review instincts have missed, and what does the question that caught it have in common with the other three?
2. You marked several classes absent. Which of those absences rests on evidence, and which on the fact that you had not yet built the surface where it would appear?

### AR-02 — review of the supplied bad system (D-w08-2)

Rungs: `DL-4` debug, `DL-8` explain.

#### Objective

Find defects somebody else planted, in code that reads well, and demonstrate that
your review skill transfers off your own repository.

#### Task

Read `SUP-01` above and review it against all fourteen classes. For each defect
you claim, produce evidence: the specific lines, and where possible a
reproduction — a second call, an injected process death, two concurrent runs.
Write the review as an architecture decision record naming which classes are
present, with evidence per class.

#### Constraints

- The planted-defect list at the head of `SUP-01` may not be consulted until the review is written and committed.
- A claimed defect needs line-level evidence. "This looks risky" is not a finding.
- At least two defects must be evidenced by a reproduction rather than by reading alone, since reading is what these defects were built to survive.
- Classes you find absent are recorded as absent, so the review has a denominator.

#### Deliverable

`D-w08-2` — an **ADR** (`DT-04`): the review of `SUP-01` against the fourteen
classes, with evidence per named defect and the reproductions attached.

#### Acceptance criteria

- All 14 classes are assessed and recorded as present or absent.
- At least 4 of the 6 planted defects are identified before the list is consulted.
- At least 2 findings are supported by a reproduction, not by reading.
- 100% of identified defects cite at least 1 specific line range.

#### Metrics

- Success rate: planted defects found divided by 6.
- Failure rate: claimed defects that are not present divided by defects claimed.

#### Reflection questions

1. Which planted defect did you miss, and what would have had to be true about your process for you to have caught it?
2. The code passes a linter and has high coverage. What does that tell you about the relationship between the signals you usually trust and the defects that actually matter here?

### AR-03 — self-inspection of the full platform (D-w12-3)

Rungs: `DL-8` explain.

#### Objective

Review the whole platform through `S7b` with the five-axis rubric, and produce a
result credible enough that a reader who dislikes you would accept it.

#### Task

Formalise the four recurring questions into the five-axis rubric —
correctness under repetition, crash-window durability, concurrency, contract and
boundary assumptions, and privilege — then review the full platform against the
fourteen classes using it. Name at least two defects you are **accepting**, each
with a remediation plan and a target month.

#### Constraints

- At least two accepted defects must be named. A clean bill of health on a system this size is the least credible possible output and fails this exercise on that ground.
- Each accepted defect carries a remediation month, not an intention.
- The rubric scores five axes independently. One aggregate verdict is a different instrument and does not satisfy this.
- Findings from AR-01 that were never remediated are re-reported rather than quietly dropped.

#### Deliverable

`D-w12-3` — an **ADR** (`DT-04`): the full-platform review conducted with the
five-axis rubric, naming accepted defects with remediation months.

#### Acceptance criteria

- All 5 axes are scored independently, each with its own citation.
- At least 2 defects are recorded as accepted, each with a named remediation month.
- All 14 classes are assessed against the full platform.
- Every AR-01 finding is marked remediated, accepted, or re-reported, with 0 dropped silently.

#### Metrics

- Success rate: AR-01 findings closed divided by AR-01 findings recorded.
- Test coverage: proportion of the accepted defects that have a failing test standing in for the missing fix.

#### Reflection questions

1. You accepted two defects. What would have to change — in load, in users, or in who runs this — for one of them to stop being acceptable?
2. Compare this review with AR-01. Did the platform get better, or did your review get better, and what evidence separates the two?
