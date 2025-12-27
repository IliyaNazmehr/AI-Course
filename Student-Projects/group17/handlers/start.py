"""
handlers/start.py
Handles the `/start` command and initial user onboarding.
If a user is new, it forces a language selection.
If a user exists, it shows the main menu.
"""

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import database
from utils.i18n import get_translation as t
import logging

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle the /start command.
    Checks if user exists. If not, asks for language. If yes, shows main menu.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    # Check existence
    user_exists = await database.check_user_exists(user_id)
    if not user_exists:
        # CLEANUP: Ensure no old buttons are visible for a new user
        # We send a temporary message to remove the keyboard, then delete it.
        temp_msg = await context.bot.send_message(
            chat_id=chat_id, text="...", reply_markup=ReplyKeyboardRemove()
        )
        await context.bot.delete_message(
            chat_id=chat_id, message_id=temp_msg.message_id
        )
        # Show First Run Language Selection (Dual Language Welcome)
        txt_en = t("en", "welcome_first_run")
        txt_fa = t("fa", "welcome_first_run")
        full_text = f"{txt_en}\n\n────────────────\n\n{txt_fa}"
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data="start_set_lang_en"),
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="start_set_lang_fa"),
            ]
        ]
        await context.bot.send_message(
            chat_id=chat_id,
            text=full_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML,
        )
    else:
        # Existing user: Show Main Menu directly
        await show_main_menu(update, context)


async def start_lang_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles the language selection callback for NEW users.
    Saves the language and then displays the main menu.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    if data.startswith("start_set_lang_"):
        lang_code = data.split("_")[-1]
        # Save to DB (This explicitly creates the user record via update_user_setting logic)
        await database.update_user_setting(user_id, "bot_language", lang_code)
        # Delete the language selection message to clean up chat
        try:
            await query.delete_message()
        except Exception:
            pass
        # Show Main Menu (Buttons appear NOW)
        await show_main_menu(update, context)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Displays the main persistent keyboard menu (ReplyKeyboard).
    The text depends on the user's selected language.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")
    # Persistent Keyboard Layout
    keyboard_layout = [
        [KeyboardButton(t(lang, "btn_settings"))],
        [KeyboardButton(t(lang, "btn_help")), KeyboardButton(t(lang, "btn_about"))],
    ]
    markup = ReplyKeyboardMarkup(keyboard_layout, resize_keyboard=True)
    await context.bot.send_message(
        chat_id=chat_id,
        text=t(lang, "main_menu"),
        reply_markup=markup,
        parse_mode=ParseMode.HTML,
    )
