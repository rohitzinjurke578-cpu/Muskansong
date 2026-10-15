import os
import asyncio
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
from youtubesearchpython import VideosSearch


# Logging configuration
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
BOT_NAME = os.getenv("BOT_NAME", "Music Bot").strip()

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN environment variable is missing. "
        "Add BOT_TOKEN in Render Environment Variables."
    )


# /start command
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    msg = (
        f"🎵 Welcome to {BOT_NAME}!\n\n"
        "Commands:\n"
        "/play <song name> — search for a song\n"
        "/help — show commands\n\n"
        "I return search links; I do not download "
        "or redistribute copyrighted music."
    )

    if update.effective_message:
        await update.effective_message.reply_text(msg)


# /help command
async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    msg = (
        "🎧 Music Bot Help\n\n"
        "/play <song name> — find YouTube results\n"
        "/start — start the bot\n"
        "/help — show commands\n\n"
        "Example: /play Arijit Singh\n"
        "Use official or authorized sources for listening."
    )

    if update.effective_message:
        await update.effective_message.reply_text(msg)


# /play command
async def play(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    message = update.effective_message

    if message is None:
        return

    query = " ".join(context.args).strip()

    if not query:
        await message.reply_text(
            "Usage: /play <song name>\n"
            "Example: /play relaxing instrumental"
        )
        return

    status = await message.reply_text("🔎 Searching…")

    try:
        # Run the synchronous search outside the event loop.
        results = await asyncio.to_thread(
            lambda: VideosSearch(query, limit=5).result().get(
                "result", []
            )
        )

        if not results:
            await status.edit_text(
                "No results found. Try another search."
            )
            return

        lines = [f"🎵 Results for: {query}\n"]
        keyboard = []

        for item in results:
            title = item.get("title", "Untitled")
            link = item.get("link", "")
            duration = item.get("duration") or "Unknown length"
            views = item.get("viewCount", {}).get("short", "")

            lines.append(
                f"• {title}\n"
                f"  ⏱ {duration}  👁 {views}\n"
                f"  {link}"
            )

            if link:
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            title[:60],
                            url=link,
                        )
                    ]
                )

        await status.edit_text(
            "\n\n".join(lines),
            reply_markup=(
                InlineKeyboardMarkup(keyboard)
                if keyboard
                else None
            ),
            disable_web_page_preview=True,
        )

    except Exception:
        log.exception("Search failed")

        await status.edit_text(
            "Search is temporarily unavailable. "
            "Please try again in a moment."
        )


# Error handler
async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    log.error(
        "An error occurred while processing an update",
        exc_info=context.error,
    )


# Main function
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("play", play))
    app.add_error_handler(error_handler)

    log.info("Bot is starting")

    # Create an event loop for Python 3.14 compatibility.
    asyncio.set_event_loop(asyncio.new_event_loop())

    app.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
