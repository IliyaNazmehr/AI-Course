"""
handlers/settings.py
Manages the Settings Dashboard.
Includes logic for:
- Fetching and caching dynamic models from Groq.
- Displaying settings (Tone, Length, Language) with current values.
- Handling recursive menu updates (Sub-menus).
- Refreshing the main bot keyboard when language changes.
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import database
import config
import os
import time
import logging
from groq import AsyncGroq
from utils.i18n import get_translation as t

logger = logging.getLogger(__name__)
# Global cache structure to prevent rate limiting API calls for model lists
MODEL_CACHE = {"text": {}, "audio": {}, "timestamp": 0}
CACHE_DURATION = 3600  # 1 hour


async def get_groq_models():
    """
    Fetches models from Groq API and categorizes them into Text and Audio.
    Uses in-memory caching to avoid hitting API limits.
    Returns:
     tuple: (text_models_dict, audio_models_dict)
    """
    global MODEL_CACHE
    current_time = time.time()
    # Return cached models if valid
    if MODEL_CACHE["text"] and (
        current_time - MODEL_CACHE["timestamp"] < CACHE_DURATION
    ):
        return MODEL_CACHE["text"], MODEL_CACHE["audio"]
    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            return config.AVAILABLE_MODELS, config.AVAILABLE_AUDIO_MODELS
        client = AsyncGroq(api_key=api_key)
        models_list = await client.models.list()
        text_models = {}
        audio_models = {}
        for m in models_list.data:
            model_id = m.id
            # Filter out security/guard models
            if "guard" in model_id.lower():
                continue
            name = model_id.replace("-", " ").title()
            if "whisper" in model_id.lower():
                audio_models[name] = model_id
            else:
                # Manual beautification for common models
                if "llama-3.3" in model_id:
                    name = "Llama 3.3 (Latest)"
                elif "llama-3.1" in model_id:
                    name = "Llama 3.1"
                elif "mixtral" in model_id:
                    name = "Mixtral 8x7B"
                elif "gemma2" in model_id:
                    name = "Gemma 2"
                elif "deepseek" in model_id:
                    name = "DeepSeek R1"
                elif "qwen" in model_id:
                    name = "Qwen 2.5"
                text_models[name] = model_id
        if text_models or audio_models:
            MODEL_CACHE = {
                "text": dict(sorted(text_models.items())),
                "audio": dict(sorted(audio_models.items())),
                "timestamp": current_time,
            }
            return MODEL_CACHE["text"], MODEL_CACHE["audio"]
    except Exception as e:
        logger.error(f"Failed to fetch models from Groq API: {e}")
    return config.AVAILABLE_MODELS, config.AVAILABLE_AUDIO_MODELS


async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Displays the Dashboard Style Settings Menu.
    Shows current values of all settings in the message body.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    user_id = update.effective_user.id
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")

    # --- Helpers for Display Values ---
    def get_display_name(options, value, prefix_key=""):
        """Gets the readable name for a setting, trying translation first."""
        translation_key = f"{prefix_key}_{value}"
        translated_label = t(lang, translation_key)
        # If no translation found (key returned), look up in options dict
        if translated_label == translation_key:
            for label, val in options.items():
                if val == value:
                    return label
            return value
        return translated_label

    # --- Resolve Current Model Names ---
    curr_text_model_id = user_settings.get("model", "")
    curr_text_model_name = curr_text_model_id.split("-")[0].title()
    t_models, a_models = await get_groq_models()
    for name, mid in t_models.items():
        if mid == curr_text_model_id:
            curr_text_model_name = name
    curr_audio_model_id = user_settings.get("audio_model", "")
    curr_audio_model_name = curr_audio_model_id.split("-")[0].title()
    for name, mid in a_models.items():
        if mid == curr_audio_model_id:
            curr_audio_model_name = name
    # --- Resolve Other Settings ---
    curr_lang = get_display_name(
        config.SUMMARY_LANGUAGES, user_settings.get("summary_language"), "lang"
    )
    curr_len = get_display_name(
        config.LENGTH_OPTIONS, user_settings.get("length"), "len"
    )
    curr_tone = get_display_name(config.TONE_OPTIONS, user_settings.get("tone"), "tone")
    curr_bot_lang = "🇺🇸 English" if lang == "en" else "🇮🇷 فارسی"
    # Construct the Status Card
    info_text = (
        f"⚙️ <b>{t(lang,'settings_title')}</b>\n"
        f"─────────────────\n"
        f"🧠 <b>{t(lang,'select_model').split(' ')[-1]}:</b> {curr_text_model_name}\n"
        f"🎙 <b>{t(lang,'select_audio_model').split(' ')[-1]}:</b> {curr_audio_model_name}\n"
        f"🗣 <b>{t(lang,'select_lang').split(' ')[-1]}:</b> {curr_lang}\n"
        f"📏 <b>{t(lang,'select_len').split(' ')[-1]}:</b> {curr_len}\n"
        f"🎭 <b>{t(lang,'select_tone').split(' ')[-1]}:</b> {curr_tone}\n"
        f"🌐 <b>{t(lang,'select_interface').split(' ')[-1]}:</b> {curr_bot_lang}\n"
        f"─────────────────\n"
        f"<i>{t(lang,'settings_title').split(' ')[0]}...</i>"
    )
    # Settings Buttons
    keyboard_layout = [
        [
            InlineKeyboardButton(
                t(lang, "select_model"), callback_data="menu_model_text_0"
            ),
            InlineKeyboardButton(
                t(lang, "select_audio_model"), callback_data="menu_model_audio_0"
            ),
        ],
        [
            InlineKeyboardButton(t(lang, "select_lang"), callback_data="menu_sum_lang"),
            InlineKeyboardButton(t(lang, "select_len"), callback_data="menu_len"),
        ],
        [
            InlineKeyboardButton(t(lang, "select_tone"), callback_data="menu_tone"),
            InlineKeyboardButton(
                t(lang, "select_interface"), callback_data="menu_bot_lang"
            ),
        ],
        [
            InlineKeyboardButton(
                t(lang, "reset_defaults"), callback_data="reset_defaults"
            ),
            InlineKeyboardButton(t(lang, "close"), callback_data="close_settings"),
        ],
    ]
    markup = InlineKeyboardMarkup(keyboard_layout)
    if update.callback_query:
        try:
            await update.callback_query.edit_message_text(
                info_text, reply_markup=markup, parse_mode=ParseMode.HTML
            )
        except Exception:
            pass
    else:
        await update.message.reply_text(
            info_text, reply_markup=markup, parse_mode=ParseMode.HTML
        )


async def settings_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, data_override=None
) -> None:
    """
    Handles all interactions within the settings menu.
    Supports recursive calls via `data_override` to refresh menus without new user clicks.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
     data_override (str, optional): Used to simulate a specific callback data.
    """
    query = update.callback_query
    await query.answer()
    data = data_override if data_override else query.data
    user_id = query.from_user.id
    # --- RESET DEFAULTS ---
    if data == "reset_defaults":
        defaults = database.DEFAULT_SETTINGS.copy()
        if "user_id" in defaults:
            del defaults["user_id"]
        for k, v in defaults.items():
            await database.update_user_setting(user_id, k, v)
        user_settings = await database.get_user_settings(user_id)
        lang = user_settings.get("bot_language", "en")
        await query.answer(t(lang, "toast_reset"), show_alert=False)
        await settings_menu(update, context)
        return
    # --- NAVIGATION ---
    if data == "menu_main" or data == "close_settings":
        if data == "close_settings":
            from handlers.start import show_main_menu

            try:
                await query.delete_message()
            except:
                pass
            await show_main_menu(update, context)
        else:
            await settings_menu(update, context)
        return
    # --- SUBMENU BUILDER ---
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")

    async def build_submenu(
        title_key,
        options_dict,
        callback_prefix,
        current_db_value,
        translation_prefix="",
    ):
        """Helper to build consistent sub-menu pages."""
        buttons = []
        # Ensure valid active value logic
        valid_values = list(options_dict.values())
        active_value = current_db_value
        if active_value not in valid_values and valid_values:
            if "Professional" in valid_values:
                active_value = "Professional"
            elif "Medium" in valid_values:
                active_value = "Medium"
            elif "Auto" in valid_values:
                active_value = "Auto"
            else:
                active_value = valid_values[0]
        for label, value in options_dict.items():
            # Translate label if possible
            display_text = label
            if translation_prefix:
                trans_key = f"{translation_prefix}_{value}"
                trans_val = t(lang, trans_key)
                if trans_val != trans_key:
                    display_text = trans_val
            if active_value == value:
                display_label = f"✅ {display_text}"
            else:
                display_label = f"⬜️ {display_text}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        display_label, callback_data=f"{callback_prefix}{value}"
                    )
                ]
            )
        buttons.append(
            [InlineKeyboardButton(t(lang, "back"), callback_data="menu_main")]
        )
        header_text = (
            f"⚙️ <b>{t(lang,'settings_title')}</b>\n\n👇 <i>{t(lang,title_key)}:</i>"
        )
        await query.edit_message_text(
            header_text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML,
        )

    # --- MODEL PAGINATION BUILDER ---
    async def build_model_menu(model_type, page_num):
        """Helper to build paginated model selection menu."""
        text_models, audio_models = await get_groq_models()
        if model_type == "text":
            target_dict = text_models
            db_key = "model"
            title = t(lang, "title_text_model")
        else:
            target_dict = audio_models
            db_key = "audio_model"
            title = t(lang, "title_audio_model")
        current_selection = user_settings.get(db_key)
        # Default to first available if selection invalid
        if current_selection not in target_dict.values() and target_dict:
            current_selection = list(target_dict.values())[0]
        # Sort models: Active one at top, then others
        model_items = []
        selected_item = None
        other_items = []
        for label, mid in target_dict.items():
            if mid == current_selection:
                selected_item = (label, mid)
            else:
                other_items.append((label, mid))
        if selected_item:
            model_items.append(selected_item)
        model_items.extend(other_items)
        # Pagination logic
        ITEMS_PER_PAGE = 6
        total_pages = (len(model_items) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        start_idx = page_num * ITEMS_PER_PAGE
        end_idx = start_idx + ITEMS_PER_PAGE
        current_page_items = model_items[start_idx:end_idx]
        buttons = []
        for label, value in current_page_items:
            if current_selection == value:
                display_label = f"✅ {label}"
            else:
                display_label = f"⬜️ {label}"
            buttons.append(
                [
                    InlineKeyboardButton(
                        display_label, callback_data=f"set_model_{model_type}_{value}"
                    )
                ]
            )
        nav = []
        if page_num > 0:
            nav.append(
                InlineKeyboardButton(
                    "⬅️ Prev", callback_data=f"menu_model_{model_type}_{page_num-1}"
                )
            )
        if page_num < total_pages - 1:
            nav.append(
                InlineKeyboardButton(
                    "Next ➡️", callback_data=f"menu_model_{model_type}_{page_num+1}"
                )
            )
        if nav:
            buttons.append(nav)
        buttons.append(
            [InlineKeyboardButton(t(lang, "back"), callback_data="menu_main")]
        )
        subtitle = t(lang, "subtitle_model")
        await query.edit_message_text(
            f"⚙️ <b>{title}</b> (Page {page_num+1}/{total_pages})\n\n<i>{subtitle}</i>",
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML,
        )

    # --- ROUTING ---
    if data == "menu_sum_lang":
        await build_submenu(
            "select_lang",
            config.SUMMARY_LANGUAGES,
            "set_sum_lang_",
            user_settings.get("summary_language"),
            "lang",
        )
    elif data == "menu_len":
        await build_submenu(
            "select_len",
            config.LENGTH_OPTIONS,
            "set_len_",
            user_settings.get("length"),
            "len",
        )
    elif data == "menu_tone":
        await build_submenu(
            "select_tone",
            config.TONE_OPTIONS,
            "set_tone_",
            user_settings.get("tone"),
            "tone",
        )
    elif data == "menu_bot_lang":
        opts = {"🇺🇸 English": "en", "🇮🇷 فارسی": "fa"}
        await build_submenu(
            "select_interface", opts, "set_bot_lang_", user_settings.get("bot_language")
        )
    elif data.startswith("menu_model_text_"):
        page = int(data.split("_")[-1])
        await build_model_menu("text", page)
    elif data.startswith("menu_model_audio_"):
        page = int(data.split("_")[-1])
        await build_model_menu("audio", page)
    # --- SAVE ACTIONS ---
    if data.startswith("set_model_text_"):
        val = data.replace("set_model_text_", "")
        await database.update_user_setting(user_id, "model", val)
        await settings_callback(update, context, data_override="menu_model_text_0")
        return
    if data.startswith("set_model_audio_"):
        val = data.replace("set_model_audio_", "")
        await database.update_user_setting(user_id, "audio_model", val)
        await settings_callback(update, context, data_override="menu_model_audio_0")
        return
    mapping = {
        "set_sum_lang_": ("summary_language", "menu_sum_lang"),
        "set_len_": ("length", "menu_len"),
        "set_tone_": ("tone", "menu_tone"),
        "set_bot_lang_": ("bot_language", "menu_main"),
    }
    for prefix, (db_key, return_menu) in mapping.items():
        if data.startswith(prefix):
            val = data.replace(prefix, "")
            await database.update_user_setting(user_id, db_key, val)
            if db_key == "bot_language":
                # Special Logic: Update Bottom Buttons (Reply Keyboard)
                # We must send a new message to update the ReplyKeyboard.
                from handlers.start import show_main_menu

                # 1. Delete the old settings panel to keep chat clean
                try:
                    await query.delete_message()
                except:
                    pass
                # 2. Send the Main Menu (which updates the bottom buttons to new language)
                await show_main_menu(update, context)
                # 3. Re-open the Settings Dashboard (so user doesn't lose context)
                await settings_menu(update, context)
            else:
                await settings_callback(update, context, data_override=return_menu)
            return
