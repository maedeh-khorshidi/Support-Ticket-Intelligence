from pathlib import Path


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

APP_DIR = PROJECT_ROOT / "app"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
KNOWLEDGE_BASE_DIR = DATA_DIR / "knowledge_base"

MODEL_DIR = PROJECT_ROOT / "models"

RESULTS_DIR = PROJECT_ROOT / "results"
METRICS_DIR = RESULTS_DIR / "metrics"
CONFUSION_MATRIX_DIR = RESULTS_DIR / "confusion_matrices"
ERROR_ANALYSIS_DIR = RESULTS_DIR / "error_analysis"

EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"

# Create directories if they do not exist.
for directory in [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    KNOWLEDGE_BASE_DIR,
    MODEL_DIR,
    METRICS_DIR,
    CONFUSION_MATRIX_DIR,
    ERROR_ANALYSIS_DIR,
    EXPERIMENTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


# ============================================================
# Dataset
# ============================================================

DATASET_NAME = "PolyAI/banking77"

TRAIN_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "PolyAI-LDN/task-specific-datasets/master/"
    "banking_data/train.csv"
)

TEST_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "PolyAI-LDN/task-specific-datasets/master/"
    "banking_data/test.csv"
)

RAW_TRAIN_FILE = RAW_DATA_DIR / "banking77_train.csv"
RAW_TEST_FILE = RAW_DATA_DIR / "banking77_test.csv"

PROCESSED_DATA_FILE = (
    PROCESSED_DATA_DIR / "banking77_processed.csv"
)

# ============================================================
# Reproducibility
# ============================================================

RANDOM_SEED = 42


# ============================================================
# Text Processing
# ============================================================

TEXT_COLUMNS = ["subject", "body"]

# Maximum number of characters used when combining ticket text.
MAX_TEXT_LENGTH = 4000


# ============================================================
# Train / Validation / Test
# ============================================================

TRAIN_SIZE = 0.80
VALIDATION_SIZE = 0.10
TEST_SIZE = 0.10


# ============================================================
# Transformer
# ============================================================

BASE_TRANSFORMER_MODEL = "distilbert-base-uncased"

MAX_TOKEN_LENGTH = 256

TRAIN_BATCH_SIZE = 16
EVAL_BATCH_SIZE = 32

LEARNING_RATE = 2e-5
NUM_EPOCHS = 3
WEIGHT_DECAY = 0.01

EARLY_STOPPING_PATIENCE = 2


# ============================================================
# Sentence Transformer / Retrieval
# ============================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K_RETRIEVAL = 5


# ============================================================
# Classification
# ============================================================

CLASSIFICATION_TASKS = [
    "queue",
    "priority",
    "type",
]


# ============================================================
# Evaluation
# ============================================================

EVALUATION_AVERAGE = "weighted"

TOP_K_VALUES = [1, 3, 5, 10]


# ============================================================
# RAG
# ============================================================

RAG_TOP_K = 5

MAX_RETRIEVED_TICKETS = 5


# ============================================================
# Automation
# ============================================================

INCOMING_TICKETS_DIR = DATA_DIR / "incoming_tickets"
PROCESSED_TICKETS_DIR = DATA_DIR / "processed_tickets"

INCOMING_TICKETS_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_TICKETS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Pipeline
# ============================================================

MAX_RETRIES = 3