"""Cheap, model-free query signals. No network or embedding call is needed."""
import re

COMPARISON = {"compare", "versus", "vs", "difference", "tradeoff", "pros", "cons"}
MULTIHOP = {"why", "how", "impact", "relationship", "affect", "cause", "steps", "pipeline", "architecture"}
FRESH = {"today", "latest", "current", "recent", "now", "2026"}

def extract_features(query: str) -> dict[str, float]:
    q=query.lower().strip(); words=re.findall(r"[a-z0-9]+", q)
    question_count=max(1, sum(q.count(x) for x in ["?", " and ", " also "]))
    return {
      "word_count": min(len(words)/35, 1.0),
      "char_count": min(len(q)/240, 1.0),
      "question_count": min(question_count/3, 1.0),
      "comparison_signal": float(bool(COMPARISON.intersection(words))),
      "reasoning_signal": float(bool(MULTIHOP.intersection(words))),
      "freshness_signal": float(bool(FRESH.intersection(words))),
      "constraint_signal": float(any(x in q for x in ["under ", "at least", "unless", "except", "within", "condition"])) ,
      "entity_count": min(len(set(w for w in words if len(w)>1))/30, 1.0),
      "definition_signal": float(q.startswith(("what is ", "define ", "who is ", "meaning of "))),
      "conversational_signal": float(len(words)<8 and not COMPARISON.intersection(words) and not MULTIHOP.intersection(words)),
    }
