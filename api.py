from fastapi import FastAPI
from pydantic import BaseModel, Field
from retrievaliq.knowledge import load_documents
from retrievaliq.engine import RetrievalIQ
app=FastAPI(title="RetrievalIQ API",version="1.0.0",description="Query-adaptive retrieval with trace and cost telemetry")
engine=RetrievalIQ(load_documents())
class AskRequest(BaseModel): query:str=Field(min_length=2,max_length=2000); strategy:str="adaptive"
@app.get("/health")
def health(): return {"status":"ok","service":"retrievaliq"}
@app.post("/ask")
def ask(body:AskRequest):
    if body.strategy not in {"adaptive","always","fixed","direct"}: return {"error":"strategy must be adaptive, always, fixed, or direct"}
    return engine.ask(body.query,body.strategy).to_dict()
