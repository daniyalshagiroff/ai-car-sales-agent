import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

SHEET_URL = os.getenv("SHEET_URL", "").strip()
SHEET_NAME = os.getenv("SHEET_NAME", "").strip()
SHEET_WORKSHEET = os.getenv("SHEET_WORKSHEET", "Cars").strip()
SERVICE_JSON_PATH = os.getenv("GSPREAD_SERVICE_ACCOUNT_JSON", "service_account.json")

DEFAULT_TOP_N = int(os.getenv("DEFAULT_TOP_N", "5"))

SYSTEM_PROMPT = (
    "You are a senior Sales Manager at SMP Motors (luxury dealership in Dubai). "
    "Reply ONLY in English. Tone: professional, concise, strictly on-topic. "
    "No long paragraphs. Always: 1) reference concrete inventory options if available, "
    "2) clarify price/status, 3) end with a clear call-to-action (book a viewing/test-drive or share contact). "
    "If the exact request isn't available, propose closest alternatives."
)