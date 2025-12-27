"""
utils/i18n.py
Internationalization (i18n) module.
Contains a dictionary `STRINGS` mapping language codes ('en', 'fa') to UI text strings.
Includes logic for new user welcome messages and error handling text.
"""

STRINGS = {
    "en": {
        "welcome_first_run": (
            "👋 <b>Welcome to AI Summarizer!</b>\n\n"
            "I can summarize text, audio, and documents for you.\n"
            "<i>To get started, please select your language:</i>"
        ),
        "main_menu": (
            "🤖 <b>AI Summarizer Assistant</b>\n\n"
            "I am ready to turn your content into clear, concise insights.\n\n"
            "<b>👇 Send me any of the following:</b>\n"
            "📝 <b>Text:</b> Paste articles or long messages.\n"
            "🎙 <b>Audio:</b> Forward voice notes or music/podcast files.\n"
            "📄 <b>Files:</b> Upload PDF, DOCX, or EPUB documents.\n\n"
            "<i>Select an option below to configure the bot:</i>"
        ),
        "processing": "⏳ <b>Processing...</b>\n<i>The AI is analyzing your content...</i>",
        "downloading": "📥 <b>Downloading file...</b>",
        "transcribing": "🎙 <b>Transcribing Audio...</b>\n<i>Converting speech to text. This may take a moment.</i>",
        "extracting": "📄 <b>Reading Document...</b>\n<i>Extracting text from the file.</i>",
        "summary_header": "📝 <b>Summary Result:</b>",
        "error_generic": "❌ <b>An error occurred.</b>\nPlease try again later or contact support.",
        "error_file": "❌ <b>File Error.</b>\nThe file is empty, password-protected, or the format is not supported.",
        "error_format": "❌ <b>Unsupported Audio.</b>\nI can only process MP3, OGG, WAV, and M4A formats.",
        "error_api": "❌ <b>API Error.</b>\nCould not reach the AI service. Please try again later.",
        "settings_title": "Configuration Dashboard",
        "btn_settings": "⚙️ Settings",
        "btn_help": "❓ User Guide",
        "btn_about": "ℹ️ About",
        "select_model": "🧠 Text Model",
        "select_audio_model": "🎙 Audio Model",
        "select_lang": "🗣 Summary Language",
        "select_len": "📏 Length",
        "select_tone": "🎭 Tone",
        "select_interface": "🌐 Bot Language",
        "back": "🔙 Back",
        "close": "🔙 Back to Main Menu",
        "redo": "🔄 Regenerate",
        "reset_defaults": "🔄 Reset Defaults",
        "toast_reset": "✅ Settings have been reset to default.",
        "tone_Professional": "Professional",
        "tone_Academic": "Academic",
        "tone_ELI5": "Simple (ELI5)",
        "tone_Friendly": "Friendly",
        "tone_Journalistic": "Journalistic",
        "tone_Witty": "Witty",
        "len_Short": "Short (Bullets)",
        "len_Medium": "Medium",
        "len_Long": "Long (Detailed)",
        "lang_Auto": "Auto Detect",
        "lang_English": "English",
        "lang_Persian": "Persian",
        "title_text_model": "Text Summarization Model",
        "title_audio_model": "Audio Transcription Model",
        "subtitle_model": "Active model is always shown at the top.",
        "help_text": (
            "<b>❓ User Guide</b>\n\n"
            "Here is how to maximize your use of this bot:\n\n"
            "<b>1. Text Summarization</b>\n"
            "Simply paste any long text into this chat. The bot will detect the language and provide a summary.\n\n"
            "<b>2. Document Analysis</b>\n"
            "Upload <b>PDF, DOCX, or EPUB</b> files. Perfect for analyzing books, reports, or papers.\n\n"
            "<b>3. Audio Intelligence</b>\n"
            "Forward voice notes or upload audio files (e.g., meeting recordings). The bot will transcribe and summarize them.\n\n"
            "<b>⚙️ Customization</b>\n"
            "Use the <b>Settings</b> menu to control:\n"
            "• <b>Tone:</b> Make the output Professional, Witty, Academic, etc.\n"
            "• <b>Length:</b> Choose between Bullet Points (Short) or Detailed Paragraphs (Long).\n"
            "• <b>Target Language:</b> Automatically translate the summary into your preferred language."
        ),
        "about_text": (
            "<b>ℹ️ About AI Summarizer</b>\n\n"
            "<b>Version:</b> 4.1.0\n"
            "<b>Engine:</b> Groq Inference API\n\n"
            "This bot utilizes state-of-the-art Large Language Models (LLMs) such as <b>Llama 3.3</b>, <b>Mixtral</b>, and <b>DeepSeek</b> to provide human-level comprehension.\n\n"
            "<b>🔒 Privacy & Security:</b>\n"
            "We prioritize your privacy. Files and text are processed in real-time and are <b>never stored</b> on our servers after processing is complete.\n\n"
            "<i>Designed for speed and accuracy.</i>"
        ),
    },
    "fa": {
        "welcome_first_run": (
            "👋 <b>به ربات هوشمند خلاصه‌ساز خوش آمدید!</b>\n\n"
            "من می‌توانم متن‌ها، صداها و اسناد شما را تحلیل و خلاصه کنم.\n"
            "<i>برای شروع، لطفاً زبان مورد نظر خود را انتخاب کنید:</i>"
        ),
        "main_menu": (
            "🤖 <b>دستیار هوشمند خلاصه‌سازی</b>\n\n"
            "من آماده‌ام تا محتوای شما را به چکیده‌ای دقیق و مفید تبدیل کنم.\n\n"
            "<b>👇 یکی از موارد زیر را ارسال کنید:</b>\n"
            "📝 <b>متن:</b> مقالات یا پیام‌های طولانی خود را بفرستید.\n"
            "🎙 <b>صدا:</b> پیام صوتی (ویس) یا فایل صوتی ارسال کنید.\n"
            "📄 <b>فایل:</b> اسناد PDF، DOCX یا کتاب‌های EPUB را آپلود کنید.\n\n"
            "<i>برای تنظیمات بیشتر، یکی از دکمه‌های زیر را انتخاب کنید:</i>"
        ),
        "processing": "⏳ <b>در حال پردازش...</b>\n<i>هوش مصنوعی در حال تحلیل محتواست...</i>",
        "downloading": "📥 <b>در حال دانلود فایل...</b>",
        "transcribing": "🎙 <b>در حال تبدیل صدا به متن...</b>\n<i>لطفاً شکیبا باشید، این کار ممکن است کمی زمان ببرد.</i>",
        "extracting": "📄 <b>در حال خواندن سند...</b>\n<i>استخراج متن از فایل ارسالی.</i>",
        "summary_header": "📝 <b>خلاصه نهایی:</b>",
        "error_generic": "❌ <b>خطایی رخ داد.</b>\nلطفاً دقایقی دیگر تلاش کنید یا با پشتیبانی تماس بگیرید.",
        "error_file": "❌ <b>خطای فایل.</b>\nفایل ارسالی خالی است، رمز دارد یا فرمت آن پشتیبانی نمی‌شود.",
        "error_format": "❌ <b>فرمت نامعتبر.</b>\nمن تنها از فایل‌های صوتی استاندارد (MP3, OGG, WAV, M4A) پشتیبانی می‌کنم.",
        "error_api": "❌ <b>خطای سرویس.</b>\nارتباط با سرویس هوش مصنوعی برقرار نشد. لطفاً بعداً تلاش کنید.",
        "settings_title": "پنل تنظیمات و پیکربندی",
        "btn_settings": "⚙️ تنظیمات",
        "btn_help": "❓ راهنما",
        "btn_about": "ℹ️ درباره ربات",
        "select_model": "🧠 مدل متنی",
        "select_audio_model": "🎙 مدل صوتی",
        "select_lang": "🗣 زبان خلاصه",
        "select_len": "📏 طول متن",
        "select_tone": "🎭 لحن و سبک",
        "select_interface": "🌐 زبان ربات",
        "back": "🔙 بازگشت",
        "close": "🔙 بازگشت به منوی اصلی",
        "redo": "🔄 تلاش مجدد",
        "reset_defaults": "🔄 بازگشت به پیش‌فرض",
        "toast_reset": "✅ تنظیمات به حالت اولیه بازگشت.",
        "tone_Professional": "رسمی و اداری",
        "tone_Academic": "علمی و آکادمیک",
        "tone_ELI5": "ساده (برای کودکان)",
        "tone_Friendly": "دوستانه و صمیمی",
        "tone_Journalistic": "خبری و روزنامه‌نگاری",
        "tone_Witty": "شوخ‌طبع و خلاقانه",
        "len_Short": "کوتاه (نکته‌وار)",
        "len_Medium": "متوسط",
        "len_Long": "طولانی (با جزئیات)",
        "lang_Auto": "تشخیص خودکار",
        "lang_English": "انگلیسی",
        "lang_Persian": "فارسی",
        "title_text_model": "مدل خلاصه‌سازی متنی",
        "title_audio_model": "مدل تبدیل گفتار به نوشتار",
        "subtitle_model": "مدل فعال همیشه در بالای لیست نمایش داده می‌شود.",
        "help_text": (
            "<b>❓ راهنمای جامع استفاده</b>\n\n"
            "برای بهترین استفاده از ربات، به نکات زیر توجه کنید:\n\n"
            "<b>۱. خلاصه‌سازی متن</b>\n"
            "کافیست متن طولانی، مقاله یا خبر را در چت کپی کنید. ربات به صورت خودکار آن را تحلیل و خلاصه می‌کند.\n\n"
            "<b>۲. تحلیل اسناد</b>\n"
            "فایل‌های <b>PDF, DOCX یا EPUB</b> را ارسال کنید. این قابلیت برای خواندن سریع مقالات دانشگاهی یا گزارش‌ها عالی است.\n\n"
            "<b>۳. هوش مصنوعی صوتی</b>\n"
            "ویس‌ها یا فایل‌های صوتی جلسات را فوروارد کنید. ربات ابتدا آن را به متن تبدیل کرده و سپس نکات کلیدی را استخراج می‌کند.\n\n"
            "<b>⚙️ تنظیمات پیشرفته</b>\n"
            "از منوی <b>تنظیمات</b> می‌توانید رفتار ربات را تغییر دهید:\n"
            "• <b>لحن:</b> انتخاب لحن رسمی، دوستانه، علمی و ...\n"
            "• <b>طول:</b> انتخاب بین خلاصه کوتاه (نکته‌وار) یا کامل (پاراگرافی).\n"
            "• <b>زبان مقصد:</b> ترجمه همزمان خلاصه نهایی به فارسی یا انگلیسی."
        ),
        "about_text": (
            "<b>ℹ️ درباره ربات</b>\n\n"
            "<b>نسخه:</b> ۴.۱.۰\n"
            "<b>موتور پردازش:</b> Groq Inference API\n\n"
            "این ربات از قدرتمندترین مدل‌های زبانی جهان (LLM) مانند <b>Llama 3.3</b>، <b>Mixtral</b> و <b>DeepSeek</b> بهره می‌برد تا درکی در سطح انسان ارائه دهد.\n\n"
            "<b>🔒 امنیت و حریم خصوصی:</b>\n"
            "ما به حریم خصوصی شما احترام می‌گذاریم. تمامی فایل‌ها و پیام‌ها به صورت آنی پردازش شده و پس از اتمام کار، <b>بلافاصله از سرورها حذف می‌شوند</b>.\n\n"
            "<i>طراحی شده برای سرعت و دقت.</i>"
        ),
    },
}


def get_translation(user_lang: str, key: str) -> str:
    """
    Retrieves the translated string for a specific key and language code.
    Defaults to 'en' if language is missing, and returns key itself if translation is missing.
    Args:
     user_lang (str): User's language code ('en' or 'fa').
     key (str): The string key to lookup.
    Returns:
     str: Translated text.
    """
    lang = user_lang if user_lang in STRINGS else "en"
    return STRINGS[lang].get(key, key)
