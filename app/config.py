"""Environment configuration and secure project paths."""
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parent.parent
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / '.env', extra='ignore')
    OLLAMA_BASE_URL: str = 'http://localhost:11434'
    CHAT_MODEL: str = 'llama3.2'
    EMBEDDING_MODEL: str = 'nomic-embed-text'
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150
    RETRIEVAL_TOP_K: int = 4
    DEMO_MODE: bool = True
    DEMO_REVIEWER_TOKEN: str = 'replace-with-long-random-local-token'

@lru_cache
def get_settings() -> Settings:
    return Settings()

DOCUMENTS_DIR = ROOT / 'documents'
OUTPUT_DIR = ROOT / 'output'
DOCUMENTS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
