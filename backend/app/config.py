from pathlib import Path

import os

from types import SimpleNamespace

from dotenv import load_dotenv


# Load .env
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")


# Paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


DATASET_PATH = DATA_DIR / "dataset.csv"
METADATA_PATH = DATA_DIR / "metadata.json"


# Environment variables
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "")


def get_settings():
    return SimpleNamespace(
        DATA_DIR=str(DATA_DIR),
        DATASET_PATH=str(DATASET_PATH),
        METADATA_PATH=str(METADATA_PATH),
        LLM_PROVIDER=LLM_PROVIDER,
        GROQ_API_KEY=GROQ_API_KEY,
        OPENAI_API_KEY=OPENAI_API_KEY,
        LOCAL_MODEL_PATH=LOCAL_MODEL_PATH,
    )
