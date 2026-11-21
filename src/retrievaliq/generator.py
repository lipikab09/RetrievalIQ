"""Grounded extractive mode by default; optional OpenAI-compatible chat completion."""
import os, re, urllib.request, json
from .config import SETTINGS

def generate_answer(query, chunks):
    if SETTINGS.generation_mode.lower()=="openai" and SETTINGS.openai_api_key:
        return _remote_answer(query,chunks)
    if not chunks:
        return ("This looks answerable without consulting the local knowledge base. "
                "For a domain-specific or time-sensitive answer, add trusted source documents and enable retrieval.")
    qterms=set(re.findall(r"[a-z0-9]+",query.lower())); ranked=[]
    for c in chunks:
        for sentence in re.split(r"(?<=[.!?])\s+",c.text):
            overlap=len(qterms & set(re.findall(r"[a-z0-9]+",sentence.lower())))
            if overlap: ranked.append((overlap,sentence.strip(),c.title))
    ranked.sort(reverse=True)
    seen=set(); lines=[]
    for _,s,title in ranked:
        if s and s not in seen: lines.append(f"• {s} [{title}]"); seen.add(s)
        if len(lines)>=4: break
    return "\n".join(lines) if lines else "I found related documents, but not enough direct evidence to answer confidently. Try a more specific question."

def _remote_answer(query,chunks):
    context="\n\n".join(f"[{c.title}] {c.text}" for c in chunks)
    payload={"model":SETTINGS.openai_model,"temperature":0.1,"messages":[
      {"role":"system","content":"Answer only from supplied context. If context is absent or insufficient, say so. Cite source titles inline."},
      {"role":"user","content":f"Question: {query}\n\nContext:\n{context}"}]}
    req=urllib.request.Request(SETTINGS.openai_base_url.rstrip("/")+"/chat/completions",data=json.dumps(payload).encode(),headers={"Authorization":f"Bearer {SETTINGS.openai_api_key}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as r: return json.loads(r.read())["choices"][0]["message"]["content"]
