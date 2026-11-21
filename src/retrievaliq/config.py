from dataclasses import dataclass
import os
from dotenv import load_dotenv
load_dotenv()

@dataclass(frozen=True)
class Settings:
    generation_mode: str = os.getenv("GENERATION_MODE", "extractive")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    cost_per_1k_tokens_usd: float = 0.00015
    latency_budget_ms: int = 1800
SETTINGS = Settings()
