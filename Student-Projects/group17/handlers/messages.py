"""
handlers/messages.py
Handles incoming Text Messages and the Summarization Logic.
Logic:
1. Intercepts "Menu Buttons" (Settings, Help, About).
2. Routes text content to the Summarization Engine.
3. Handles the 'redo' callback to regenerate summaries.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from groq import AsyncGroq
import os
import database
import config
from utils.i18n import get_translation as t
from utils.text_processing import send_smart_chunked_message
import logging

logger = logging.getLogger(__name__)
# Initialize Async Client
groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))


async def handle_text_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Entry point for text messages.
    Routes to specific menus if button text matches, otherwise treats as input for summarization.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    user_id = update.effective_user.id
    text_content = update.message.text
    # Async DB Call to get user preferences
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")
    # --- Robust Button Interception ---
    # We check against ALL supported languages to ensure buttons work
    # even if the user interface state is slightly out of sync.
    is_settings = text_content in [t("en", "btn_settings"), t("fa", "btn_settings")]
    is_help = text_content in [t("en", "btn_help"), t("fa", "btn_help")]
    is_about = text_content in [t("en", "btn_about"), t("fa", "btn_about")]
    if is_settings:
        from handlers.settings import (
            settings_menu,
        )  # Lazy import to avoid circular dependency

        await settings_menu(update, context)
        return
    elif is_help:
        await update.message.reply_text(t(lang, "help_text"), parse_mode=ParseMode.HTML)
        return
    elif is_about:
        await update.message.reply_text(
            t(lang, "about_text"), parse_mode=ParseMode.HTML
        )
        return
    # --- Summarization Logic ---
    # If not a button, assume it's text to summarize
    context.user_data["last_text"] = text_content
    wait_message = await update.message.reply_text(
        t(lang, "processing"), parse_mode=ParseMode.HTML
    )
    await process_summary(user_id, text_content, wait_message, context)


async def redo_summary_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles the 'Regenerate' (Redo) button click.
    Retrieves the last processed text from context.user_data and runs the summary again.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    last_text = context.user_data.get("last_text")
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")
    if not last_text:
        # If session data is lost (bot restart), inform user
        await query.edit_message_text(
            t(lang, "error_generic") + " (Session expired)", parse_mode=ParseMode.HTML
        )
        return
    # Update message to indicate processing
    await query.edit_message_text(t(lang, "processing"), parse_mode=ParseMode.HTML)
    # Reuse the query message object for the output
    await process_summary(user_id, last_text, query.message, context)


async def process_summary(
    user_id: int, input_text: str, message_obj, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Core summarization logic.
    1. Fetches user configuration (Tone, Length, Language).
    2. Constructs the System Prompt.
    3. Calls Groq API.
    4. Sends result (chunked if long).
    Args:
     user_id (int): Telegram User ID.
     input_text (str): The text to summarize.
     message_obj: The message object to edit/reply to.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    try:
        user_settings = await database.get_user_settings(user_id)
        lang = user_settings.get("bot_language", "en")
        # Construct Language Instruction
        if user_settings.get("summary_language") != "Auto":
            language_instruction = (
                f"Output language: {user_settings['summary_language']}"
            )
        else:
            language_instruction = "Keep original language."
        # Get Tone Instruction (Map Short Key -> Long Prompt)
        tone_key = user_settings.get("tone", "Professional")
        tone_instruction = config.TONE_PROMPTS.get(
            tone_key, config.TONE_PROMPTS["Professional"]
        )
        # Format System Prompt
        system_content = config.SYSTEM_PROMPT.format(
            tone=tone_instruction,
            length=user_settings.get("length", "Medium"),
            language_instruction=language_instruction,
        )
        # Call Groq API
        chat_completion = await groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": f"Text to summarize:\n{input_text}"},
            ],
            model=user_settings.get("model", "llama-3.3-70b-versatile"),
            temperature=float(
                config.CREATIVITY_LEVELS.get(user_settings.get("creativity"), 0.5)
            ),
            max_tokens=2048,
        )
        summary_result = chat_completion.choices[0].message.content
        # Add "Redo" button for quick regeneration
        keyboard = [[InlineKeyboardButton(t(lang, "redo"), callback_data="redo")]]
        final_header = t(lang, "summary_header")
        full_response = f"{final_header}\n\n{summary_result}"
        # Use smart chunking to handle Telegram limits
        await send_smart_chunked_message(
            message_obj,
            full_response,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML,
        )
    except Exception as e:
        logger.error(f"Summarization API Error: {e}")
        user_settings = await database.get_user_settings(user_id)
        await message_obj.edit_text(
            t(user_settings.get("bot_language", "en"), "error_generic"),
            parse_mode=ParseMode.HTML,
        )
