from __future__ import annotations
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from config import TELEGRAM_BOT_TOKEN, DEFAULT_TOP_N
from sheets import fetch_inventory
from inventory import find_best_matches, compact_card, build_llm_context
from llm import ask_llm

WELCOME = (
    "Hi! I'm SMP Motors assistant.\n"
    "Tell me what you're looking for (brand/model/year/budget). I’ll reply in English."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = (update.message.text or "").strip()
    try:
        inv = fetch_inventory()
        matches = find_best_matches(inv, user_text, top_n=DEFAULT_TOP_N)

        if matches:
            cards = "\n\n".join(compact_card(r) for r in matches)
            await update.message.reply_text(cards, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

        llm_ctx = build_llm_context(matches)
        answer = ask_llm(llm_ctx, user_text)
        await update.message.reply_text(answer, disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text("Temporary issue reading inventory. Please try again.")
        print("ERROR:", e)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing in .env")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
