# ============================================================
#  CONFIGURATION FILE (config.py)
#  Clean, validated, production-ready for AI Follow-Up Agent
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------
# REQUIRED CONFIGS (Fail if missing)
# ------------------------------------------------------------

def require_env(key):
    value = os.getenv(key)
    if not value or value.strip() == "":
        raise ValueError(f"❌ Missing required environment variable: {key}")
    return value


# Google Sheets
SPREADSHEET_ID = require_env("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "Sheet1").strip()

# Gmail
GMAIL_FROM = require_env("GMAIL_FROM")
GMAIL_APP_PASSWORD = require_env("GMAIL_APP_PASSWORD")

# System Info
FROM_NAME = os.getenv("FROM_NAME", "Your Company").strip()
DEFAULT_SUBJECT = os.getenv("DEFAULT_SUBJECT", "Quick question about your interest").strip()


# ------------------------------------------------------------
# OLLAMA SETTINGS
# ------------------------------------------------------------

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()

# Normalize URL (remove trailing slash if present)
if OLLAMA_HOST.endswith("/"):
    OLLAMA_HOST = OLLAMA_HOST[:-1]

OLLAMA_MODEL = require_env("OLLAMA_MODEL")


# ------------------------------------------------------------
# OPENROUTER FALLBACK SETTINGS
# ------------------------------------------------------------

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()

# If user provided API key → validate URL
if OPENROUTER_API_KEY:
    OPENROUTER_URL = "https://openrouter.ai/v1/chat/completions"
else:
    OPENROUTER_URL = None  # disables fallback cleanly


# ------------------------------------------------------------
# FOLLOW-UP TIMING (in days)
# ------------------------------------------------------------

FOLLOWUP_DAYS = {
    "day0": 0,
    "day1": 1,
    "day3": 3,
    "day7": 7
}

# ------------------------------------------------------------
# PRINT SUMMARY AT LOAD (optional)
# ------------------------------------------------------------

print("\n===== CONFIG LOADED SUCCESSFULLY =====")
print(f"Spreadsheet: {SPREADSHEET_ID}")
print(f"Sheet Name:  {SHEET_NAME}")
print(f"Email From:  {GMAIL_FROM}")
print(f"Ollama Host: {OLLAMA_HOST}")
print(f"Ollama Model:{OLLAMA_MODEL}")
print(f"OpenRouter:  {'Enabled' if OPENROUTER_API_KEY else 'Disabled'}")
print("=====================================\n")
