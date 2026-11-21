"""Interpretable retrieval-budget router with a conservative uncertainty fallback."""
from .features import extract_features
from .models import RouteDecision

class AdaptiveRouter:
    def __init__(self, thresholds=None):
        self.thresholds=thresholds or {"skip":0.16,"shallow":0.34,"medium":0.62}

    def decide(self, query: str) -> RouteDecision:
        f=extract_features(query)
        # Weighted score is intentionally inspectable; tune on held-out data, not intuition alone.
        score=(0.25*f["word_count"] + 0.15*f["char_count"] + 0.10*f["question_count"] +
               0.25*f["comparison_signal"] + 0.28*f["reasoning_signal"] +
               0.10*f["constraint_signal"] + 0.10*f["entity_count"] +
               0.10*f["freshness_signal"] - 0.08*f["definition_signal"] -
               0.10*f["conversational_signal"])
        score=max(0.0,min(1.0,score))
        # Greetings and purely conversational prompts should not pay retrieval cost.
        if f["conversational_signal"] and len(query.split())<=5:
            route,k,reason="DIRECT",0,"Short conversational query; retrieval is unlikely to add evidence."
        elif score < self.thresholds["skip"]:
            route,k,reason="DIRECT",0,"Low estimated evidence demand; answer without retrieval."
        elif score < self.thresholds["shallow"]:
            route,k,reason="LIGHT",2,"A small evidence set should be sufficient."
        elif score < self.thresholds["medium"]:
            route,k,reason="BALANCED",4,"Moderate reasoning or constraints justify broader context."
        else:
            route,k,reason="DEEP",7,"High complexity signal; allocate a larger evidence budget."
        # Confidence is a routing-margin proxy, not a calibrated probability.
        boundaries=sorted(self.thresholds.values())
        margin=min(abs(score-b) for b in boundaries) if boundaries else 0.5
        confidence=round(min(.99,.55+margin*1.4),3)
        return RouteDecision(route,k,confidence,round(score,3),reason,f)
