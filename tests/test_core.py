from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from retrievaliq.knowledge import load_documents
from retrievaliq.engine import RetrievalIQ
from retrievaliq.router import AdaptiveRouter

def test_short_greeting_skips_retrieval():
 d=AdaptiveRouter().decide("hey there")
 assert d.k==0 and d.route=="DIRECT"

def test_complex_query_gets_context():
 d=AdaptiveRouter().decide("Compare the architecture, tradeoffs and impact of hybrid retrieval and reranking")
 assert d.k>=4

def test_engine_trace_and_baselines():
 e=RetrievalIQ(load_documents()); r=e.ask("What is retrieval augmented generation?")
 assert r.answer and "router" in [x["stage"] for x in r.trace]
 assert e.ask("hi", "direct").metrics["chunks"]==0

def test_retrieval_returns_documents():
 e=RetrievalIQ(load_documents()); assert len(e.retriever.search("BM25 ranking",3))==3
