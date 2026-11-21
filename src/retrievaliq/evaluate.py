"""Paired benchmark runner. Metrics are computed from the included labelled toy corpus."""
import json, time
from pathlib import Path
import pandas as pd
from .knowledge import load_documents
from .engine import RetrievalIQ

def run_benchmark(output="runs/benchmark.csv"):
    root=Path(__file__).resolve().parents[2]; cases=json.loads((root/"data"/"benchmark.json").read_text())
    engine=RetrievalIQ(load_documents()); rows=[]
    for case in cases:
      for strategy in ["adaptive","always","fixed","direct"]:
        result=engine.ask(case["query"],strategy)
        retrieved={x["document_id"] for x in result.chunks}
        relevant=set(case["relevant_ids"])
        recall=len(retrieved&relevant)/len(relevant) if relevant else 1.0
        rows.append({"id":case["id"],"query":case["query"],"strategy":strategy,"route":result.decision["route"],
          "chunks":result.metrics["chunks"],"latency_ms":result.metrics["latency_ms"],"estimated_cost_usd":result.metrics["estimated_cost_usd"],
          "recall_at_k":recall,"retrieval_skipped":result.metrics["retrieval_saved"]})
    df=pd.DataFrame(rows); out=root/output; out.parent.mkdir(exist_ok=True,parents=True); df.to_csv(out,index=False)
    summary=df.groupby("strategy").agg(queries=("id","count"),avg_latency_ms=("latency_ms","mean"),avg_chunks=("chunks","mean"),avg_estimated_cost_usd=("estimated_cost_usd","mean"),mean_recall_at_k=("recall_at_k","mean"),skip_rate=("retrieval_skipped","mean")).round(4)
    summary.to_csv(out.with_name("summary.csv")); return summary,df
