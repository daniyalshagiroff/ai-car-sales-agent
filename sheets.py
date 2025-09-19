from __future__ import annotations
import os
import gspread
from typing import List, Dict
from google.oauth2.service_account import Credentials
from config import SERVICE_JSON_PATH, SHEET_URL, SHEET_NAME, SHEET_WORKSHEET

COLS = ["Car Name", "Price", "Color", "Mileage", "Features", "Status"]

def _authorize():
    if not SERVICE_JSON_PATH:
        raise RuntimeError("Set GSPREAD_SERVICE_ACCOUNT_JSON in .env to point to your Google service account JSON file.")

    service_path = os.path.abspath(SERVICE_JSON_PATH)
    if not os.path.exists(service_path):
        raise RuntimeError(f"Service account file not found: {service_path}")
    if os.path.getsize(service_path) == 0:
        raise RuntimeError(f"Service account file is empty: {service_path}")

    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = Credentials.from_service_account_file(service_path, scopes=scopes)
    return gspread.authorize(creds)

def _open_worksheet():
    gc = _authorize()
    if SHEET_URL:
        sh = gc.open_by_url(SHEET_URL)
    elif SHEET_NAME:
        sh = gc.open(SHEET_NAME)
    else:
        raise RuntimeError("Provide SHEET_URL or SHEET_NAME in .env")
    return sh.worksheet(SHEET_WORKSHEET)

def fetch_inventory() -> List[Dict]:
    ws = _open_worksheet()
    rows = ws.get_all_records()  
    inv: List[Dict] = []
    for r in rows:
        def get(k: str) -> str:
            if k in r: 
                return str(r.get(k, "")).strip()
            for kk, vv in r.items():
                if kk.lower().strip() == k.lower():
                    return str(vv).strip()
            return ""
        inv.append({
            "name": get("Car Name"),
            "price": get("Price"),
            "color": get("Color"),
            "mileage": get("Mileage"),
            "features": get("Features"),
            "status": get("Status"),
        })
    return inv