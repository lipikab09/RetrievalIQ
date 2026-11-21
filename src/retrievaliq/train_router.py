"""Train a lightweight supervised route classifier from labelled JSONL.
Expected records: {"query": "...", "label": "DIRECT|LIGHT|BALANCED|DEEP"}.
Use grouped/temporal splits for real data; this starter uses stratified holdout.
"""
import argparse,json,pickle
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from .features import extract_features

def main():
 p=argparse.ArgumentParser(); p.add_argument("dataset",help="JSONL labelled routing examples"); p.add_argument("--out",default="models/router.pkl"); a=p.parse_args()
 rows=[json.loads(x) for x in Path(a.dataset).read_text().splitlines() if x.strip()]
 X=[extract_features(x["query"]) for x in rows]; y=[x["label"].upper() for x in rows]
 if len(set(y))<2: raise SystemExit("Need at least two route classes")
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
 model=Pipeline([("vectorizer",DictVectorizer()),("classifier",LogisticRegression(max_iter=1000,class_weight="balanced"))]); model.fit(Xtr,ytr)
 print(classification_report(yte,model.predict(Xte),zero_division=0)); out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); pickle.dump(model,out.open("wb")); print(f"Saved {out}")
if __name__=="__main__": main()
