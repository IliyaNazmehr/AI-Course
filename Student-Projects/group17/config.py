"""
config.py
This module contains all configuration constants, model definitions,
and system prompts used throughout the bot.
It acts as a central repository for easy adjustments to the
bot's behavior.
"""

# --- GROQ MODELS ---
# A fallback list of text generation models.
# The bot attempts to fetch the live list from Groq API first, using this only if that fails.
AVAILABLE_MODELS = {
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Llama 3.1 8B": "llama-3.1-8b-instant",
    "Llama 3 70B": "llama3-70b-8192",
    "Llama 3 8B": "llama3-8b-8192",
    "Mixtral 8x7B": "mixtral-8x7b-32768",
    "Gemma 2 9B": "gemma2-9b-it",
    "DeepSeek R1 Distill 70B": "deepseek-r1-distill-llama-70b",
    "Qwen 2.5 32B": "qwen-2.5-32b",
    "Llama 3.2 90B Vision": "llama-3.2-90b-vision-preview",
}
# --- AUDIO MODELS ---
# Whisper models supported by Groq for transcription.
AVAILABLE_AUDIO_MODELS = {
    "Whisper Large V3": "whisper-large-v3",
    "Whisper Large V3 Turbo": "whisper-large-v3-turbo",
    "Distil-Whisper English": "distil-whisper-large-v3-en",
}
# --- SUMMARIZATION SETTINGS ---
# Maps display names to internal codes for target languages.
SUMMARY_LANGUAGES = {
    "🤖 Auto Detection": "Auto",
    "🇺🇸 English": "English",
    "🇮🇷 Persian (Farsi)": "Persian",
    "🇪🇸 Spanish": "Spanish",
    "🇫🇷 French": "French",
    "🇩🇪 German": "German",
    "🇷🇺 Russian": "Russian",
    "🇸🇦 Arabic": "Arabic",
    "🇹🇷 Turkish": "Turkish",
    "🇨🇳 Chinese": "Chinese",
}
# Settings for summary length.
LENGTH_OPTIONS = {
    "⚡ Short (Bullets)": "Short",
    "📝 Medium (Balanced)": "Medium",
    "📜 Long (Detailed)": "Long",
}
# --- TONE SETTINGS ---
#'TONE_OPTIONS': Short keys used for Database storage and Button callbacks (limited by 64 bytes).
TONE_OPTIONS = {
    "👔 Professional": "Professional",
    "🎓 Academic": "Academic",
    "🧸 ELI5 (Simple)": "ELI5",
    "👋 Friendly": "Friendly",
    "📰 Journalistic": "Journalistic",
    "😜 Witty": "Witty",
}
#'TONE_PROMPTS': Maps the short keys above to detailed instructions for the System Prompt.
TONE_PROMPTS = {
    "Professional": "Professional, objective, and executive-style",
    "Academic": "Academic, analytical, and formal",
    "ELI5": "Simple, easy-to-understand (Explain Like I'm 5)",
    "Friendly": "Friendly, conversational, and warm",
    "Journalistic": "Journalistic, factual, and headline-focused",
    "Witty": "Witty, humorous, and engaging",
}
# Temperature settings for the LLM to control randomness.
CREATIVITY_LEVELS = {"Precise": 0.1, "Balanced": 0.5, "Creative": 0.8}
# --- SYSTEM PROMPTS ---
# The core instruction sent to the LLM.
# It strictly forbids unsupported HTML tags to prevent Telegram parsing errors.
SYSTEM_PROMPT = """
You are an elite AI summarization assistant.
Your goal is to synthesize the input text into a clear, high-quality summary strictly adhering to the user's configuration.

--- CONFIGURATION ---
1. **Tone**: Adopt a {tone} tone.
2. **Length**: The summary must be {length}.
3. **Language**: {language_instruction}

--- OUTPUT REQUIREMENTS ---
- **Format**: HTML compatible with Telegram.
- **Allowed Tags**: ONLY use <b>, <i>, <u>, <s>, <code>, <pre>.
- **Forbidden Tags**: Do NOT use <p>, <br>, <h1>, <ul>, <li>, or <div>.
- **Structure**:
  - Use double newlines for paragraph breaks.
  - Use "• " (bullet character) for lists, NOT HTML list tags.
- **Constraints**:
  - Do NOT use Markdown (like ** or ##).
  - Do NOT include conversational filler (e.g., "Here is the summary").
  - Output ONLY the summary content.

Analyze the text deeply and provide the best possible summary now.
"""
