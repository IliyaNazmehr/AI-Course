# Advanced AI Summarizer Bot (Groq)

An advanced Telegram bot that leverages Groq's high-speed LLM API to summarize text. This bot allows users to customize the summarization style, length, tone, and language, persisting user preferences via a local database.

## 🚀 Features

* **Multi-Model Support:** Switch between powerful models like `Llama 3.3 70B`, `Llama 3.1 8B`, `Mixtral 8x7B`, and `Gemma 2 9B`.
* **Customizable Summaries:**
    * **Length:** Short (Bullets), Medium (Standard), Long (Detailed).
    * **Tone:** Professional, Casual, ELI5 (Explain Like I'm 5).
    * **Creativity:** Adjust temperature from Precise (0.1) to Creative (0.8).
* **Multilingual:** Supports Auto-detection, English, Persian, Spanish, French, German, Chinese, Russian, and Arabic.
* **User Persistence:** Automatically saves user preferences using SQLite so settings are remembered for future interactions.
* **Interactive UI:** Easy-to-use Inline Keyboard menus for settings and configuration.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** `python-telegram-bot` (v21.10)
* **AI Provider:** Groq API
* **Database:** SQLite3
* **Environment:** `python-dotenv`

## ⚙️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Set up Virtual Environment**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Create a `.env` file in the root directory. You can copy the structure from the example below:
    
    **File:** `.env`
    ```ini
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
    GROQ_API_KEY=your_groq_api_key_here
    ```

    * Get your **Bot Token** from [@BotFather](https://t.me/BotFather) on Telegram.
    * Get your **Groq API Key** from the [Groq Console](https://console.groq.com/).

## ▶️ Usage

1.  **Run the Bot**
    ```bash
    python bot.py
    ```

2.  **Interact on Telegram**
    * Send `/start` to initialize the bot and see the main menu.
    * Click **⚙️ Settings** to configure your preferred Model, Language, and Tone.
    * **Send any text** to the bot, and it will generate a summary based on your saved settings.
    * Use the **🔄 Redo / Regenerate** button to get a new version of the summary.

## 📂 Project Structure

```text
├── bot.py           # Main entry point and bot logic
├── config.py        # Configuration, constants, and prompt templates
├── database.py      # SQLite database handling (user settings)
├── requirements.txt # Python dependencies
├── .env             # Environment variables (API Keys)
├── .gitignore       # Files to ignore (venv, db, logs, etc.)
└── bot_users.db     # Generated at runtime (stores user data)

```

## 👥 Authors

1. **Alireza Alem**
2. **Nadia Karami**
3. **Melina Malakjan**
4. 
5. 

## 📄 License

This project is open-source and available under the MIT License.
