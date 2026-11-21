from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Document:
    id: str
    title: str
    text: str
    source: str = "local knowledge base"

@dataclass
class RouteDecision:
    route: str
    k: int
    confidence: float
    complexity: float
    reason: str
    features: dict[str, float]

@dataclass
class RetrievedChunk:
    document_id: str
    title: str
    text: str
    score: float
    source: str

@dataclass
class QueryResult:
    query: str
    answer: str
    decision: dict[str, Any]
    chunks: list[dict[str, Any]]
    metrics: dict[str, Any]
    trace: list[dict[str, Any]]
    def to_dict(self): return asdict(self)
