"""
bot.py
The entry point of the application.
1. Loads environment variables.
2. Initializes the Database.
3. Registers all command and message handlers.
4. Starts the polling loop.
"""

import os
import logging
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    Application,
)
import database
from handlers import start, messages, files, settings

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def post_init(application: Application) -> None:
    """Async hook to initialize the database before the bot starts polling."""
    logger.info("Initializing Database...")
    await database.init_db()
    logger.info("Database Initialized.")


if __name__ == "__main__":
    # 1. Check Token
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.critical("Error: TELEGRAM_BOT_TOKEN not found in .env file.")
        exit(1)
    # 2. Build Application
    app = ApplicationBuilder().token(token).post_init(post_init).build()
    # 3. Register Handlers
    # Commands
    app.add_handler(CommandHandler("start", start.start_command))
    app.add_handler(CommandHandler("settings", settings.settings_menu))
    # First-Run Language Callback (Specific pattern)
    app.add_handler(
        CallbackQueryHandler(start.start_lang_callback, pattern="^start_set_lang_")
    )
    # File & Audio Handlers
    app.add_handler(
        MessageHandler(filters.VOICE | filters.AUDIO, files.handle_voice_audio)
    )
    app.add_handler(MessageHandler(filters.Document.ALL, files.handle_document))
    # Redo/Regenerate Callback - FIXED: Added specific handler for redo
    app.add_handler(
        CallbackQueryHandler(messages.redo_summary_callback, pattern="^redo$")
    )
    # General Settings Callback (Catches all other callbacks)
    app.add_handler(CallbackQueryHandler(settings.settings_callback))
    # Text Message Handler (Must be last to avoid catching commands)
    app.add_handler(
        MessageHandler(filters.TEXT & (~filters.COMMAND), messages.handle_text_message)
    )
    # 4. Run Bot
    logger.info("Bot is running...")
    app.run_polling()
