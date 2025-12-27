"""
utils/text_processing.py
Handles the extraction of text from various file formats (PDF, DOCX, EPUB)
and provides utilities for sanitizing HTML output to ensure Telegram compatibility.
"""

import io
import logging
import uuid
import os
import re
import pypdf
from docx import Document
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)


def extract_text_from_file(file_bytes: bytes, file_ext: str) -> Optional[str]:
    """
    Extracts raw text from binary file data based on extension.
    Args:
     file_bytes (bytes): The file content.
     file_ext (str): The extension (e.g., .pdf).
    Returns:
     Optional[str]: Extracted text or None on failure.
    """
    try:
        if file_ext == ".pdf":
            reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            text_pages = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_pages.append(text)
            return "\n".join(text_pages)
        elif file_ext == ".docx":
            doc = Document(io.BytesIO(file_bytes))
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_ext == ".epub":
            # Ebooklib typically requires a file path, so we write to a temp file.
            # Using UUID to prevent collision in concurrent requests.
            temp_filename = f"temp_{uuid.uuid4()}.epub"
            try:
                with open(temp_filename, "wb") as temp_file:
                    temp_file.write(file_bytes)
                book = epub.read_epub(temp_filename)
                text_content = []
                for item in book.get_items():
                    if item.get_type() == ebooklib.ITEM_DOCUMENT:
                        # Use BeautifulSoup to strip HTML tags from EPUB content
                        soup = BeautifulSoup(item.get_content(), "html.parser")
                        text_content.append(soup.get_text())
                return "\n".join(text_content)
            finally:
                # Cleanup temp file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
        elif file_ext == ".txt":
            return file_bytes.decode("utf-8", errors="ignore")
    except Exception as e:
        logger.error(f"Text Extraction Error for {file_ext}: {e}")
        return None
    return None


def sanitize_html(text: str) -> str:
    """
    Cleans up HTML to ensure it is compatible with Telegram's limited HTML parser.
    Removes unsupported tags like <p>, <div>, <br> and converts headers/lists to visual equivalents.
    Args:
     text (str): Raw HTML or text.
    Returns:
     str: Sanitized text.
    """
    if not text:
        return ""
    # Replace block-level tags with newlines
    text = text.replace("<p>", "").replace("</p>", "\n\n")
    text = text.replace("<br>", "\n").replace("<br/>", "\n")
    text = text.replace("<ul>", "").replace("</ul>", "\n")
    text = text.replace("<ol>", "").replace("</ol>", "\n")
    text = text.replace("<li>", "• ").replace("</li>", "\n")
    # Convert Headers to Bold
    text = re.sub(r"<h[1-6]>(.*?)</h[1-6]>", r"<b>\1</b>\n", text)
    # Strip generic containers
    text = text.replace("<div>", "").replace("</div>", "")
    return text.strip()


async def send_smart_chunked_message(
    update_obj, text: str, reply_markup=None, parse_mode="HTML"
):
    """
    Splits long messages (>4096 chars) into chunks to avoid Telegram API errors.
    Tries to split by double newline (paragraph), then single newline, then space.
    Args:
     update_obj: The telegram message or callback_query object to reply to.
     text: The full text to send.
     reply_markup: Optional keyboard to attach to the LAST chunk.
     parse_mode: The parse mode (HTML).
    """
    # Sanitize first to prevent parse errors from the LLM output
    text = sanitize_html(text)
    MAX_LENGTH = 4000  # Safety buffer below 4096
    if len(text) <= MAX_LENGTH:
        try:
            # Try editing if it's an edit-capable object, else fall back to reply
            await update_obj.edit_text(
                text=text, reply_markup=reply_markup, parse_mode=parse_mode
            )
        except Exception:
            await update_obj.reply_text(
                text=text, reply_markup=reply_markup, parse_mode=parse_mode
            )
        return
    # Split logic
    chunks = []
    while text:
        if len(text) <= MAX_LENGTH:
            chunks.append(text)
            break
        # Find best split point
        split_index = text.rfind("\n\n", 0, MAX_LENGTH)
        if split_index == -1:
            split_index = text.rfind("\n", 0, MAX_LENGTH)
        if split_index == -1:
            split_index = text.rfind(" ", 0, MAX_LENGTH)
        if split_index == -1:
            split_index = MAX_LENGTH
        chunks.append(text[:split_index])
        text = text[split_index:].strip()
    # Send chunks
    # First chunk replaces "Processing..." message
    await update_obj.edit_text(text=chunks[0], parse_mode=parse_mode)
    # Subsequent chunks are sent as new messages
    for i, chunk in enumerate(chunks[1:]):
        # Attach the keyboard only to the very last chunk
        markup = reply_markup if i == len(chunks[1:]) - 1 else None
        await update_obj.reply_text(
            text=chunk, reply_markup=markup, parse_mode=parse_mode
        )
