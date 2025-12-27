"""
database.py
Handles all asynchronous interactions with the SQLite database (`bot_users.db`).
Uses `aiosqlite` to ensure database operations do not block the main Telegram bot event loop.
"""

import aiosqlite
import logging
from typing import Dict, Any, Optional

DB_NAME = "bot_users.db"
logger = logging.getLogger(__name__)
# Default user settings applied when a new user is created.
DEFAULT_SETTINGS = {
    "model": "llama-3.3-70b-versatile",
    "audio_model": "whisper-large-v3",
    "summary_language": "Auto",
    "length": "Medium",
    "tone": "Professional",
    "creativity": "Balanced",
    "bot_language": "en",
}


async def init_db() -> None:
    """
    Initialize the SQLite database asynchronously.
    Creates the `user_settings` table if it does not exist.
    Also performs a migration check to add the `audio_model` column for existing databases.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            # Create table with default constraints
            await db.execute(
                """
    CREATE TABLE IF NOT EXISTS user_settings (
     user_id INTEGER PRIMARY KEY,
     model TEXT DEFAULT 'llama-3.3-70b-versatile',
     audio_model TEXT DEFAULT 'whisper-large-v3',
     summary_language TEXT DEFAULT 'Auto',
     length TEXT DEFAULT 'Medium',
     tone TEXT DEFAULT 'Professional',
     creativity TEXT DEFAULT 'Balanced',
     bot_language TEXT DEFAULT 'en'
    )
    """
            )
            # Simple migration: Attempt to add audio_model if it was missing in older versions.
            # If it exists, this silently fails (caught by try/except), which is acceptable here.
            try:
                await db.execute(
                    "ALTER TABLE user_settings ADD COLUMN audio_model TEXT DEFAULT 'whisper-large-v3'"
                )
            except Exception:
                pass
            await db.commit()
    except Exception as e:
        logger.error(f"Database initialization error: {e}")


async def check_user_exists(user_id: int) -> bool:
    """
    Checks if a user already has a record in the database.
    Args:
     user_id (int): Telegram User ID.
    Returns:
     bool: True if user exists, False otherwise.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            async with db.execute(
                "SELECT 1 FROM user_settings WHERE user_id = ?", (user_id,)
            ) as cursor:
                return await cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"Error checking user existence {user_id}: {e}")
        return False


async def get_user_settings(user_id: int) -> Dict[str, Any]:
    """
    Fetch user settings asynchronously.
    Args:
     user_id (int): Telegram User ID.
    Returns:
     Dict: A dictionary of user settings. Returns defaults if user not found.
    """
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            db.row_factory = aiosqlite.Row  # Allows accessing columns by name
            async with db.execute(
                "SELECT * FROM user_settings WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
            if row:
                return dict(row)
            else:
                # Return default dictionary wrapper without writing to DB yet
                defaults = DEFAULT_SETTINGS.copy()
                defaults["user_id"] = user_id
                return defaults
    except Exception as e:
        logger.error(f"Error fetching settings for {user_id}: {e}")
        return DEFAULT_SETTINGS.copy()


async def update_user_setting(user_id: int, key: str, value: Any) -> None:
    """
    Update or Insert a specific setting for a user using an UPSERT strategy.
    Args:
     user_id (int): Telegram User ID.
     key (str): The column name to update.
     value (Any): The new value.
    """
    try:
        # Fetch current state to ensure valid values for other columns during insert
        current_settings = await get_user_settings(user_id)
        current_settings[key] = value
        async with aiosqlite.connect(DB_NAME) as db:
            # UPSERT: Insert, or Update if Conflict on Primary Key (user_id)
            await db.execute(
                """
    INSERT INTO user_settings (user_id, model, audio_model, summary_language, length, tone, creativity, bot_language)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
     model=excluded.model,
     audio_model=excluded.audio_model,
     summary_language=excluded.summary_language,
     length=excluded.length,
     tone=excluded.tone,
     creativity=excluded.creativity,
     bot_language=excluded.bot_language
    """,
                (
                    user_id,
                    current_settings.get("model", DEFAULT_SETTINGS["model"]),
                    current_settings.get(
                        "audio_model", DEFAULT_SETTINGS["audio_model"]
                    ),
                    current_settings.get(
                        "summary_language", DEFAULT_SETTINGS["summary_language"]
                    ),
                    current_settings.get("length", DEFAULT_SETTINGS["length"]),
                    current_settings.get("tone", DEFAULT_SETTINGS["tone"]),
                    current_settings.get("creativity", DEFAULT_SETTINGS["creativity"]),
                    current_settings.get(
                        "bot_language", DEFAULT_SETTINGS["bot_language"]
                    ),
                ),
            )
            await db.commit()
    except Exception as e:
        logger.error(f"Error updating setting {key} for {user_id}: {e}")
