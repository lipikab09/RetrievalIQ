"""Adaptive retrieval with evidence sufficiency escalation and auditable traces."""
import time
from .router import AdaptiveRouter
from .retriever import HybridRetriever
from .generator import generate_answer
from .models import QueryResult

class RetrievalIQ:
    def __init__(self, documents):
        self.router=AdaptiveRouter(); self.retriever=HybridRetriever(documents)

    def ask(self, query: str, strategy="adaptive") -> QueryResult:
        start=time.perf_counter(); trace=[]; decision=self.router.decide(query)
        if strategy=="always": route,k,reason="DEEP",7,"Baseline: always retrieve top 7."
        elif strategy=="fixed": route,k,reason="FIXED",4,"Baseline: always retrieve top 4."
        elif strategy=="direct": route,k,reason="DIRECT",0,"Baseline: never retrieve."
        else: route,k,reason=decision.route,decision.k,decision.reason
        trace.append({"stage":"router","route":route,"k":k,"reason":reason,"complexity":decision.complexity})
        chunks=self.retriever.search(query,k) if k else []
        trace.append({"stage":"retrieval","retrieved":len(chunks),"top_score":chunks[0].score if chunks else 0})
        # Evidence gate: low top score or thin coverage permits one bounded escalation.
        if strategy=="adaptive" and chunks and k<7:
            coverage=sum(1 for c in chunks if c.score>=0.18)
            if chunks[0].score<0.24 or coverage==0:
                new_k=min(7,max(k+2,4)); chunks=self.retriever.search(query,new_k)
                trace.append({"stage":"evidence_gate","action":"escalate","new_k":new_k,"reason":"Initial evidence signal below sufficiency threshold."})
            else: trace.append({"stage":"evidence_gate","action":"stop","reason":"Initial evidence passed sufficiency threshold."})
        elif strategy=="adaptive": trace.append({"stage":"evidence_gate","action":"skip" if not chunks else "budget_cap"})
        answer=generate_answer(query,chunks)
        elapsed=(time.perf_counter()-start)*1000
        # Transparent proxy accounting; not a provider invoice or real token bill.
        prompt_tokens=sum(max(1,len(c.text.split())) for c in chunks)+len(query.split())
        metrics={"latency_ms":round(elapsed,2),"retrieval_calls":1 if k else 0,"chunks":len(chunks),
          "estimated_context_tokens":prompt_tokens,"estimated_cost_usd":round(prompt_tokens/1000*0.00015,8),
          "retrieval_saved":k==0,"strategy":strategy}
        trace.append({"stage":"generation","mode":"extractive/local","answer_chars":len(answer)})
        return QueryResult(query,answer,{"route":route,"k":k,"confidence":decision.confidence,"complexity":decision.complexity,"reason":reason,"features":decision.features},[c.__dict__ for c in chunks],metrics,trace)
