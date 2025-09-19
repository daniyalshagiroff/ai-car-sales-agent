from __future__ import annotations
import textwrap
from openai import OpenAI
from config import OPENAI_API_KEY, SYSTEM_PROMPT

client = OpenAI(api_key=OPENAI_API_KEY)

def ask_llm(inventory_context: str, user_message: str) -> str:
    content = textwrap.dedent(f"""
    INVENTORY (from Google Sheets, subset):
    {inventory_context}

    USER MESSAGE:
    {user_message}

    INSTRUCTIONS:
    - Answer in English only, 3-6 sentences max.
    - If items exist, reference 1-3 concrete options (name + price/status).
    - If price is empty -> say "Price on request".
    - Finish with a clear CTA (book a viewing/test drive or share contact).
    """).strip()

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content}
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content.strip()
