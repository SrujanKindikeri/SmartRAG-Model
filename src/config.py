"""
=========================================================
SmartRAG Configuration
=========================================================

Central configuration for the entire SmartRAG project.

Project Structure
-----------------
SmartRAG/
│
├── data/
├── logs/
├── metadata/
├── models/
├── src/
├── vector_db/
└── history.json
=========================================================
"""

from pathlib import Path

# =========================================================
# Project Paths
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

MODELS_DIR = PROJECT_ROOT / "models"

METADATA_DIR = PROJECT_ROOT / "metadata"

LOG_DIR = PROJECT_ROOT / "logs"

INDEX_FILE = METADATA_DIR / "index.json"

MEMORY_FILE = PROJECT_ROOT / "history.json"

# =========================================================
# Create Required Directories
# =========================================================

for directory in [
    DATA_DIR,
    VECTOR_DB_DIR,
    MODELS_DIR,
    METADATA_DIR,
    LOG_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

# =========================================================
# Chunking Configuration
# =========================================================

CHUNK_SIZE = 500

CHUNK_OVERLAP = 100

# =========================================================
# Embedding Model
# =========================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

EMBEDDING_BATCH_SIZE = 32

# =========================================================
# ChromaDB
# =========================================================

COLLECTION_NAME = "smartrag"

TOP_K = 5

RERANK_TOP_K = 3

# =========================================================
# Cross Encoder
# =========================================================

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# =========================================================
# Ollama
# =========================================================

OLLAMA_MODEL = "qwen3:8b"

TEMPERATURE = 0.2

TOP_P = 0.9

MAX_TOKENS = 1024

# =========================================================
# Conversation Memory
# =========================================================

MAX_HISTORY = 10

MEMORY_CONTEXT_LIMIT = 3000

# =========================================================
# Logging
# =========================================================

APP_LOG = LOG_DIR / "application.log"

ERROR_LOG = LOG_DIR / "error.log"

INDEX_LOG = LOG_DIR / "index.log"

# =========================================================
# Feature Flags
# =========================================================

ENABLE_RERANK = True

ENABLE_STREAMING = True

ENABLE_INCREMENTAL_INDEXING = True

ENABLE_DUPLICATE_CHECK = True

DEBUG = True

# =========================================================
# Supported File Types
# =========================================================

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}

# =========================================================
# Prompt Settings
# =========================================================

SYSTEM_NAME = "SmartRAG"

NO_CONTEXT_RESPONSE = (
    "I couldn't find enough information in the provided documents."
)

# =========================================================
# Version
# =========================================================

VERSION = "2.0.0"