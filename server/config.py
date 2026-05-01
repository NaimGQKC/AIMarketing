import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from server directory
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Also check parent directory
    load_dotenv(Path(__file__).parent.parent / ".env")

# --- API Keys ---
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

# --- GCP / Vertex AI ---
GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "premium-bastion-492622-c7")
GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
GCP_CREDENTIALS_FILE: str = os.getenv("GCP_CREDENTIALS_FILE", str(Path(__file__).parent / "gcp-credentials.json"))
USE_VERTEX_AI: bool = os.getenv("USE_VERTEX_AI", "true").lower() == "true"

# --- Database ---
DB_PATH: str = os.getenv("DB_PATH", str(Path(__file__).parent / "visimind.db"))

# --- Server ---
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))

# --- Probing ---
PROBE_ITERATIONS: int = int(os.getenv("PROBE_ITERATIONS", "50"))
PROBE_TEMPERATURE: float = float(os.getenv("PROBE_TEMPERATURE", "0.7"))
GOLDEN_SET_VARIATIONS: int = int(os.getenv("GOLDEN_SET_VARIATIONS", "5"))
PROBE_MODEL: str = os.getenv("PROBE_MODEL", "gemini-2.5-flash")
JUDGE_MODEL: str = os.getenv("JUDGE_MODEL", "gemini-2.5-flash")

# --- Probe Volume Tiers ---
# Statistical rationale:
# At N=50 per angle (250 total), we achieve ~95% confidence interval of ±6.2% on citation rates.
# At N=200 per angle (1,000 total), CI narrows to ±3.1%.
# Scout tier (50 total) is directional only — flag this in UI.
#
# Market benchmark: Evertune runs 1M+/month, Profound runs 6M+/day.
# These tiers give us enterprise-credible sample sizes while keeping cost manageable.
PROBE_TIER: str = os.getenv("PROBE_TIER", "standard")
PROBE_TIER_MAP: dict = {
    "scout":     {"iterations": 10,  "total_probes": 50,   "label": "Scout",      "ci_label": "Directional estimate"},
    "standard":  {"iterations": 50,  "total_probes": 250,  "label": "Standard",   "ci_label": "95% CI +/-6%"},
    "enterprise":{"iterations": 200, "total_probes": 1000, "label": "Enterprise", "ci_label": "95% CI +/-3%"},
}

# --- Feature flags ---
USE_LIVE_LLM: bool = bool(GOOGLE_API_KEY)

# --- Ollama Local Inference ---
USE_OLLAMA: bool = os.getenv("USE_OLLAMA", "false").lower() == "true"
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

# --- Auth ---
SECRET_KEY: str = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    import secrets
    SECRET_KEY = secrets.token_urlsafe(32)

# --- Environment ---
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

# --- Additional API Keys ---
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", GOOGLE_API_KEY)

# --- Rate Limiting ---
DAILY_PROBE_LIMIT: int = int(os.getenv("DAILY_PROBE_LIMIT", "10"))
