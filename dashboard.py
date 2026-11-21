import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/"src"))
import streamlit as st
import pandas as pd
import plotly.express as px
from retrievaliq.knowledge import load_documents
from retrievaliq.engine import RetrievalIQ
from retrievaliq.evaluate import run_benchmark

st.set_page_config(page_title="RetrievalIQ · Adaptive Intelligence",page_icon="◈",layout="wide",initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#090b12;--panel:#111522;--muted:#8992aa;--line:#242b3d;--violet:#9b8cff;--cyan:#54d8d1}
.stApp{background:radial-gradient(ellipse at 80% -10%,#27204c 0%,#0b0d17 36%,#080a10 78%);color:#edf0fb;font-family:'Manrope',sans-serif}
.block-container{padding-top:2rem;max-width:1450px}.hero{padding:26px 30px;border:1px solid #34304f;border-radius:22px;background:linear-gradient(115deg,rgba(115,91,224,.18),rgba(28,35,57,.68));margin-bottom:20px}
.eyebrow{font:11px 'DM Mono';letter-spacing:2.5px;color:#a99cff}.hero h1{font-size:42px;letter-spacing:-2px;margin:8px 0 4px;color:#f5f4ff}.hero p{color:#aab2c8;font-size:15px;margin:0}.metric{background:linear-gradient(145deg,#171c2c,#101420);border:1px solid #2a3146;border-radius:16px;padding:17px 19px;min-height:105px}.metric .label{font:10px 'DM Mono';letter-spacing:1.4px;color:#8d98b1}.metric .value{font-size:27px;font-weight:800;margin-top:8px;color:#f5f4ff}.metric .hint{font-size:11px;color:#929bb0;margin-top:2px}.section{font-size:18px;font-weight:800;margin:12px 0;color:#f0efff}.sub{color:#929bb0;font-size:13px}.route{display:inline-block;padding:6px 11px;border-radius:99px;background:#292348;color:#c5baff;font:11px 'DM Mono';border:1px solid #51447e}
[data-testid="stSidebar"]{background:#0d101a;border-right:1px solid #252b3c}[data-testid="stSidebar"] *{color:#dce1f2}.stTextInput input,.stTextArea textarea{background:#111625!important;color:#f5f4ff!important;border:1px solid #303950!important;border-radius:12px!important}.stButton button{background:linear-gradient(100deg,#7964db,#5c9de8);color:white;border:0;border-radius:11px;font-weight:700;padding:.6rem 1.1rem}.stButton button:hover{border:1px solid #b9adff;color:white}.stTabs [data-baseweb="tab"]{color:#aeb7cc}.stTabs [aria-selected="true"]{color:#c4b8ff!important}.stAlert{background:#171b2b;border:1px solid #343b54}
hr{border-color:#242b3d}.stCaption{color:#8d96ac}
</style>""",unsafe_allow_html=True)

@st.cache_resource
def get_engine(): return RetrievalIQ(load_documents())
engine=get_engine()
with st.sidebar:
 st.markdown("## ◈ RETRIEVALIQ")
 st.caption("ADAPTIVE INTELLIGENCE ENGINE")
 page=st.radio("WORKSPACE",["Overview","Query lab","Benchmark studio","Architecture"],label_visibility="collapsed")
 st.divider(); st.markdown("**SYSTEM STATUS**")
 st.markdown("🟢 Local retrieval online")
 st.markdown("🟢 Router initialized")
 st.markdown("🟢 Knowledge base loaded")
 st.caption(f"{len(load_documents())} indexed knowledge documents")
 st.divider(); st.caption("v1.0.0 · CPU-friendly · local-first")

st.markdown('<div class="hero"><div class="eyebrow">QUERY-AWARE CONTEXT ALLOCATION / 001</div><h1>RETRIEVAL<span style="color:#a99aff">IQ</span></h1><p>Do not retrieve more. Retrieve smarter. An adaptive intelligence layer that budgets evidence per question.</p></div>',unsafe_allow_html=True)

def metric(label,value,hint): st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="hint">{hint}</div></div>',unsafe_allow_html=True)

if page=="Overview":
 st.markdown('<div class="section">The retrieval problem, quantified</div>',unsafe_allow_html=True)
 cols=st.columns(4)
 for c,(a,b,d) in zip(cols,[("ROUTING MODES","04","Direct · Light · Balanced · Deep"),("RETRIEVAL ENGINE","HYBRID","TF-IDF + BM25 + RRF fusion"),("ESCALATION","BOUNDED","Evidence sufficiency gate"),("OBSERVABILITY","TRACE","Decision · chunks · cost · latency")]):
  with c: metric(a,b,d)
 st.markdown("<br>",unsafe_allow_html=True)
 left,right=st.columns([1.15,1])
 with left:
  st.markdown('<div class="section">One query. One deliberate budget.</div><div class="sub">The router allocates context only when expected evidence value justifies it.</div>',unsafe_allow_html=True)
  st.markdown("""<div style='background:#111522;border:1px solid #293148;border-radius:16px;padding:20px;margin-top:12px'>
  <div style='display:flex;gap:10px;align-items:center;flex-wrap:wrap'><span class='route'>QUERY</span> <span style='color:#66708a'>→</span><span class='route'>FEATURE SIGNALS</span><span style='color:#66708a'>→</span><span class='route'>ROUTER</span></div>
  <div style='height:20px;border-left:1px dashed #5b547e;margin-left:30px'></div>
  <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px'>
  <div style='background:#191d2d;border:1px solid #3b365b;border-radius:10px;padding:12px;text-align:center'><b style='color:#a99aff'>DIRECT</b><br><small style='color:#929bb0'>0 chunks</small></div>
  <div style='background:#191d2d;border:1px solid #3b365b;border-radius:10px;padding:12px;text-align:center'><b style='color:#a99aff'>LIGHT</b><br><small style='color:#929bb0'>2 chunks</small></div>
  <div style='background:#191d2d;border:1px solid #3b365b;border-radius:10px;padding:12px;text-align:center'><b style='color:#a99aff'>BALANCED</b><br><small style='color:#929bb0'>4 chunks</small></div>
  <div style='background:#191d2d;border:1px solid #3b365b;border-radius:10px;padding:12px;text-align:center'><b style='color:#a99aff'>DEEP</b><br><small style='color:#929bb0'>7 chunks</small></div></div>
  <div style='height:20px;border-left:1px dashed #5b547e;margin-left:30px'></div><div style='background:#17252b;border:1px solid #2d6664;border-radius:10px;padding:12px;text-align:center;color:#83ded5'>EVIDENCE GATE · STOP OR ESCALATE</div>
  <div style='height:20px;border-left:1px dashed #5b547e;margin-left:30px'></div><div style='background:#1c2030;border:1px solid #3a4260;border-radius:10px;padding:12px;text-align:center'>GROUNDED ANSWER + AUDIT TRACE</div></div>""",unsafe_allow_html=True)
 with right:
  st.markdown('<div class="section">Why adaptive retrieval?</div>',unsafe_allow_html=True)
  st.markdown("""<div style='padding:17px;background:#111522;border:1px solid #293148;border-radius:16px;margin-top:12px'>
  <p style='color:#a99aff;font-weight:800'>01 / Avoid waste</p><p class='sub'>Greetings, definitions and simple conversational prompts can bypass the retrieval stack.</p><hr>
  <p style='color:#a99aff;font-weight:800'>02 / Spend context where needed</p><p class='sub'>Comparison, multi-constraint and multi-step questions receive a larger evidence budget.</p><hr>
  <p style='color:#a99aff;font-weight:800'>03 / Verify before stopping</p><p class='sub'>A lightweight evidence gate can escalate once when initial retrieval appears weak.</p><hr>
  <p style='color:#a99aff;font-weight:800'>04 / Measure the trade-off</p><p class='sub'>Paired baselines expose quality, context, estimated cost and latency—not just chatbot output.</p></div>""",unsafe_allow_html=True)
 st.caption("Important: this is a reproducible local-first engineering prototype. Benchmark outcomes must be measured on your machine and dataset; no performance improvement is pre-claimed.")

elif page=="Query lab":
 st.markdown('<div class="section">Live routing sandbox</div><div class="sub">Inspect the router decision, evidence budget, retrieved chunks and execution trace.</div>',unsafe_allow_html=True)
 query=st.text_area("ENTER A QUESTION",value="Compare hybrid retrieval and dense retrieval, and explain when reranking is worth its latency cost.",height=95)
 strategy=st.selectbox("EXECUTION POLICY",["adaptive","always","fixed","direct"],help="Run the same query through adaptive or baseline strategies.")
 if st.button("RUN INTELLIGENCE ENGINE",use_container_width=True):
  result=engine.ask(query,strategy); d=result.decision; m=result.metrics
  st.markdown("<br>",unsafe_allow_html=True)
  c=st.columns(4)
  for x,(a,b,e) in zip(c,[("ROUTE",d['route'],d['reason']),("BUDGET",str(d['k'])+" chunks","Initial retrieval allocation"),("LATENCY",f"{m['latency_ms']} ms","Measured wall-clock local runtime"),("EST. CONTEXT COST",f"${m['estimated_cost_usd']:.7f}","Illustrative token-price proxy")]):
   with x: metric(a,b,e)
  st.markdown('<div class="section">Generated response</div>',unsafe_allow_html=True); st.markdown(result.answer)
  st.markdown('<div class="section">Decision telemetry</div>',unsafe_allow_html=True)
  st.json({"route":d["route"],"confidence_proxy":d["confidence"],"complexity_score":d["complexity"],"features":d["features"]})
  if result.chunks:
   st.markdown('<div class="section">Retrieved evidence</div>',unsafe_allow_html=True)
   for i,ch in enumerate(result.chunks,1):
    with st.expander(f"{i:02d} · {ch['title']} · relevance {ch['score']}"):
     st.write(ch["text"]); st.caption(ch["source"])
  else: st.info("Retrieval was skipped. No document chunks were fetched.")
  st.markdown('<div class="section">Execution trace</div>',unsafe_allow_html=True); st.dataframe(pd.DataFrame(result.trace),use_container_width=True,hide_index=True)

elif page=="Benchmark studio":
 st.markdown('<div class="section">Paired evaluation laboratory</div><div class="sub">Run the same labelled query set through adaptive, always-retrieve, fixed top-4 and never-retrieve policies.</div>',unsafe_allow_html=True)
 st.warning("The included benchmark is a small synthetic demonstration set. Use a domain-specific held-out dataset before making placement or production performance claims.")
 if st.button("RUN ALL BASELINES",use_container_width=True):
  with st.spinner("Running paired experiments..."):
   summary,df=run_benchmark(); st.session_state["benchmark_summary"]=summary; st.session_state["benchmark_rows"]=df
 if "benchmark_summary" in st.session_state:
  summary=st.session_state["benchmark_summary"]; df=st.session_state["benchmark_rows"]
  st.dataframe(summary,use_container_width=True)
  a,b=st.columns(2)
  with a:
   fig=px.bar(summary.reset_index(),x="strategy",y="avg_latency_ms",title="Mean end-to-end latency",template="plotly_dark"); fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"); st.plotly_chart(fig,use_container_width=True)
  with b:
   fig=px.bar(summary.reset_index(),x="strategy",y="mean_recall_at_k",title="Mean evidence Recall@K",template="plotly_dark"); fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)"); st.plotly_chart(fig,use_container_width=True)
  st.markdown("**Per-query paired results**"); st.dataframe(df,use_container_width=True,hide_index=True)
  st.download_button("DOWNLOAD RAW RUNS CSV",df.to_csv(index=False),"retrievaliq_benchmark.csv","text/csv")
 else: st.info("Run the benchmark to populate measured results and comparison charts.")

else:
 st.markdown('<div class="section">System architecture</div>',unsafe_allow_html=True)
 st.markdown("""<div style='background:#111522;border:1px solid #293148;border-radius:16px;padding:22px'>
 <div style='text-align:center;background:#20203a;border:1px solid #51447e;padding:13px;border-radius:10px'>① QUERY INPUT</div><div style='text-align:center;color:#8d80d6;padding:8px'>↓</div>
 <div style='text-align:center;background:#18212d;border:1px solid #35516b;padding:13px;border-radius:10px'>② FEATURE EXTRACTION · lexical + structural signals</div><div style='text-align:center;color:#8d80d6;padding:8px'>↓</div>
 <div style='text-align:center;background:#20203a;border:1px solid #51447e;padding:13px;border-radius:10px'>③ ADAPTIVE ROUTER · DIRECT / LIGHT / BALANCED / DEEP</div><div style='text-align:center;color:#8d80d6;padding:8px'>↓</div>
 <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px'><div style='background:#18272a;border:1px solid #326461;padding:14px;border-radius:10px;text-align:center'>④A DIRECT PATH<br><small class='sub'>No retrieval cost</small></div><div style='background:#252039;border:1px solid #574b80;padding:14px;border-radius:10px;text-align:center'>④B HYBRID RETRIEVER<br><small class='sub'>TF-IDF + BM25 + RRF</small></div></div>
 <div style='text-align:center;color:#8d80d6;padding:8px'>↓</div><div style='text-align:center;background:#18272a;border:1px solid #326461;padding:13px;border-radius:10px'>⑤ EVIDENCE SUFFICIENCY GATE · STOP / ONE-TIME ESCALATION</div><div style='text-align:center;color:#8d80d6;padding:8px'>↓</div><div style='text-align:center;background:#20203a;border:1px solid #51447e;padding:13px;border-radius:10px'>⑥ GROUNDED ANSWER + OBSERVABILITY TRACE</div></div>""",unsafe_allow_html=True)
 st.markdown('<div class="section">Engineering decisions</div>',unsafe_allow_html=True)
 st.markdown("""| Layer | Implementation | Why it matters |
 |---|---|---|
 | Router | Interpretable weighted query features | Fast, inspectable, no extra LLM call |
 | Retrieval | TF-IDF + BM25-style scoring + Reciprocal Rank Fusion | Robust lexical hybrid baseline |
 | Budget | 0 / 2 / 4 / 7 chunks | Explicit context allocation |
 | Evidence gate | Top-score/coverage heuristic with one bounded escalation | Avoids blindly trusting first-pass retrieval |
 | Generation | Extractive local default; optional OpenAI-compatible endpoint | Runs without API keys |
 | Evaluation | Paired strategies, Recall@K, latency, context-token proxy | Reproducible trade-off analysis |
 | Interfaces | Streamlit dashboard + FastAPI | Demo and integration surface |""")
 st.caption("The current router is a transparent baseline, not a trained classifier. The included train_router.py adds a supervised sklearn model workflow for a larger labelled query set.")
