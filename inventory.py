from __future__ import annotations
from typing import List, Dict
from rapidfuzz import process, fuzz

SEARCH_FIELDS = ("name", "color", "features", "status")

def normalize_price(p: str) -> str:
    s = (p or "").strip()
    return s if s else "Price on request"

def compact_card(r: Dict) -> str:
    name = r.get("name", "")
    price = normalize_price(r.get("price", ""))
    color = r.get("color", "") or "N/A"
    mileage = r.get("mileage", "") or "N/A"
    status = r.get("status", "") or "N/A"
    feats = r.get("features", "")
    feats_short = (feats[:120] + '...') if len(feats) > 120 else feats
    lines = [
        f"<b>{name}</b> - {price}",
        f"Color: {color} | Mileage: {mileage} | Status: {status}",
    ]
    if feats_short:
        lines.append(f"Features: {feats_short}")
    return "\n".join(lines)

def build_llm_context(rows: List[Dict]) -> str:
    parts = []
    for r in rows[:6]:
        parts.append(
            f"- name:{r.get('name','')} | price:{r.get('price','')} | color:{r.get('color','')} | "
            f"mileage:{r.get('mileage','')} | status:{r.get('status','')} | features:{r.get('features','')}"
        )
    return "\n".join(parts) if parts else "No matching cars found."

def find_best_matches(inv: List[Dict], query: str, top_n: int = 5) -> List[Dict]:
    if not query or len(query.strip()) < 2:
        avail = [r for r in inv if r.get("status","").lower() in ("available","in stock","ready","available ")]
        return avail[:top_n] if avail else inv[:top_n]

    corpus = {i: " ".join([str(r.get(k,"")) for k in SEARCH_FIELDS]) for i, r in enumerate(inv)}
    results = process.extract(
        query, corpus, scorer=fuzz.WRatio, limit=min(top_n*3, len(inv))
    )

    ordered: List[Dict] = []
    for (idx, _text, score) in results:
        row = inv[idx]
        if row.get("status","").lower().strip() not in ("sold", "unavailable", "reserved"):
            ordered.append({**row, "_score": score})
        if len(ordered) >= top_n:
            break

    if not ordered:
        ordered = [{**inv[idx], "_score": score} for (idx, _text, score) in results[:top_n]]
    return ordered
