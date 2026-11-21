"""Offline hybrid lexical retrieval (TF-IDF + BM25-style term scoring + RRF)."""
import re, math
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Document, RetrievedChunk

class HybridRetriever:
    def __init__(self, documents: list[Document]):
        if not documents: raise ValueError("At least one document is required")
        self.documents=documents
        self.vectorizer=TfidfVectorizer(stop_words="english", ngram_range=(1,2), sublinear_tf=True)
        self.matrix=self.vectorizer.fit_transform([d.text for d in documents])
        self.tokens=[re.findall(r"[a-z0-9]+", d.text.lower()) for d in documents]
        self.avgdl=sum(map(len,self.tokens))/len(self.tokens)
        self.df=Counter(t for doc in self.tokens for t in set(doc))

    def search(self, query: str, k: int=5) -> list[RetrievedChunk]:
        if k<=0: return []
        qv=self.vectorizer.transform([query]); dense=(self.matrix @ qv.T).toarray().ravel()
        terms=re.findall(r"[a-z0-9]+",query.lower()); n=len(self.documents); bm=[]
        for toks in self.tokens:
            counts=Counter(toks); score=0.0; dl=len(toks)
            for term in terms:
                df=self.df.get(term,0)
                if not df: continue
                idf=math.log(1+(n-df+0.5)/(df+0.5)); tf=counts[term]
                score += idf*(tf*2.2)/(tf+1.2*(0.25+0.75*dl/max(1,self.avgdl)))
            bm.append(score)
        def ranks(scores): return sorted(range(n),key=lambda i:scores[i],reverse=True)
        dr,br=ranks(dense),ranks(bm); ds={i:r+1 for r,i in enumerate(dr)}; bs={i:r+1 for r,i in enumerate(br)}
        fused={i:1/(60+ds[i])+1/(60+bs[i]) for i in range(n)}
        order=sorted(range(n),key=lambda i:fused[i],reverse=True)[:k]
        maxs=max((fused[i] for i in order),default=1) or 1
        return [RetrievedChunk(self.documents[i].id,self.documents[i].title,self.documents[i].text,
             round(fused[i]/maxs,4),self.documents[i].source) for i in order]
