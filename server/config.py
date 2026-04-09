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

# --- Database ---
DB_PATH: str = os.getenv("DB_PATH", str(Path(__file__).parent / "visimind.db"))

# --- Server ---
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

# --- Probing ---
PROBE_ITERATIONS: int = int(os.getenv("PROBE_ITERATIONS", "3"))
PROBE_TEMPERATURE: float = float(os.getenv("PROBE_TEMPERATURE", "0.7"))
GOLDEN_SET_VARIATIONS: int = int(os.getenv("GOLDEN_SET_VARIATIONS", "5"))
PROBE_MODEL: str = os.getenv("PROBE_MODEL", "gemini-2.5-flash")
JUDGE_MODEL: str = os.getenv("JUDGE_MODEL", "gemini-2.5-flash")

# --- Feature flags ---
USE_LIVE_LLM: bool = bool(GOOGLE_API_KEY)

# --- Ollama Local Inference ---
USE_OLLAMA: bool = os.getenv("USE_OLLAMA", "false").lower() == "true"
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
