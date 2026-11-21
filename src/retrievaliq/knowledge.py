from pathlib import Path
import json
from .models import Document

def load_documents(path=None):
    path=Path(path or Path(__file__).resolve().parents[2]/"data"/"knowledge_base.json")
    raw=json.loads(path.read_text(encoding="utf-8"))
    return [Document(**x) for x in raw]
