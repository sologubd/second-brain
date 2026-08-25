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
