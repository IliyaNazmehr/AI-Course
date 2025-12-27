"""
handlers/files.py
Handles file uploads (Audio and Documents).
Logic:
1. Validates file extension.
2. Downloads file.
3. Audio: Transcribes via Groq Whisper -> Summarizes.
4. Document: Extracts text -> Summarizes.
"""

import os
import logging
import uuid
from telegram import Update
from telegram.ext import ContextTypes
import database
from utils.i18n import get_translation as t
from utils.text_processing import extract_text_from_file
from handlers.messages import process_summary, groq_client

logger = logging.getLogger(__name__)
# List of formats supported directly by Groq (Whisper)
GROQ_SUPPORTED_FORMATS = [
    ".flac",
    ".mp3",
    ".mp4",
    ".mpeg",
    ".mpga",
    ".m4a",
    ".ogg",
    ".wav",
    ".webm",
]


async def handle_voice_audio(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Handles Voice notes and Audio files.
    Uses the selected Audio Model for transcription.
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    user_id = update.effective_user.id
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")
    # Get selected audio model
    audio_model = user_settings.get("audio_model", "whisper-large-v3")
    progress_msg = await update.message.reply_text(
        t(lang, "downloading"), parse_mode="HTML"
    )
    temp_input_path = None
    try:
        # 1. Identify File Info
        audio_obj = update.message.voice or update.message.audio
        file_id = audio_obj.file_id
        if update.message.voice:
            ext = ".ogg"
        else:
            file_name = getattr(audio_obj, "file_name", "audio.mp3")
            _, ext = os.path.splitext(file_name)
            if not ext:
                ext = ".mp3"
        ext = ext.lower()
        # 2. Check Support
        if ext not in GROQ_SUPPORTED_FORMATS:
            await progress_msg.edit_text(t(lang, "error_format"), parse_mode="HTML")
            return
        # 3. Download File
        telegram_file = await context.bot.get_file(file_id)
        file_bytes = await telegram_file.download_as_bytearray()
        await progress_msg.edit_text(t(lang, "transcribing"), parse_mode="HTML")
        # 4. Save with UUID to avoid collisions
        temp_input_path = f"temp_{uuid.uuid4()}{ext}"
        with open(temp_input_path, "wb") as f:
            f.write(file_bytes)
        # 5. Transcribe via Groq Whisper (Async)
        with open(temp_input_path, "rb") as f:
            transcription = await groq_client.audio.transcriptions.create(
                file=(temp_input_path, f.read()),
                model=audio_model,
                response_format="text",
            )
        transcribed_text = str(transcription)
        if not transcribed_text.strip():
            await progress_msg.edit_text(
                t(lang, "error_generic") + " (Empty audio)", parse_mode="HTML"
            )
            return
        context.user_data["last_text"] = transcribed_text
        await progress_msg.edit_text(t(lang, "processing"), parse_mode="HTML")
        await process_summary(user_id, transcribed_text, progress_msg, context)
    except Exception as e:
        logger.error(f"Voice Processing Error: {e}")
        await progress_msg.edit_text(t(lang, "error_api"), parse_mode="HTML")
    finally:
        if temp_input_path and os.path.exists(temp_input_path):
            os.remove(temp_input_path)


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles Document uploads (PDF, DOCX, EPUB).
    Args:
     update (Update): Telegram Update object.
     context (ContextTypes.DEFAULT_TYPE): Telegram Context object.
    """
    user_id = update.effective_user.id
    user_settings = await database.get_user_settings(user_id)
    lang = user_settings.get("bot_language", "en")
    doc = update.message.document
    file_name = doc.file_name.lower() if doc.file_name else "unknown"
    ext = os.path.splitext(file_name)[1]
    if ext not in [".pdf", ".docx", ".txt", ".epub"]:
        await update.message.reply_text(t(lang, "error_file"), parse_mode="HTML")
        return
    progress_msg = await update.message.reply_text(
        t(lang, "extracting"), parse_mode="HTML"
    )
    try:
        telegram_file = await doc.get_file()
        file_bytes = await telegram_file.download_as_bytearray()
        extracted_text = extract_text_from_file(file_bytes, ext)
        if not extracted_text:
            await progress_msg.edit_text(t(lang, "error_file"), parse_mode="HTML")
            return
        context.user_data["last_text"] = extracted_text
        await progress_msg.edit_text(t(lang, "processing"), parse_mode="HTML")
        await process_summary(user_id, extracted_text, progress_msg, context)
    except Exception as e:
        logger.error(f"Document Processing Error: {e}")
        await progress_msg.edit_text(t(lang, "error_generic"), parse_mode="HTML")
