
# Group 18
Iman Hekmatpanah
sara hasan vazifeshenas
asal shafie
Faeze fereydounpour
Sevil meshkini

# Advanced Telegram Text Summarization Bot

An asynchronous Telegram bot that summarizes long texts using OpenAl's Chat Completion API.

The bot supports multiple summary styles, handles very long inputs safely, and minimizes API usage through caching.

# ## Overview

This project is a **production-ready Telegram bot** designed to summarize text messages directly inside Telegram chats.

Users simply reply to a message and choose how they want it summarized.

The bot is optimized for:

- Long texts

- High concurrency

- Cost efficiency

- Clean async architecture

# ## Features




**Async Telegram bot** using `python-telegram-bot v20+`




- ☐ **Long-text summarization** with automatic chunking



**Multiple summary modes**

- Short (2-3 sentences)

- Bullet points

- Detailed summary with headings



**SQLite caching** to avoid repeated API calls

- 0 **Concurrency limiting** using

asyncio.Semaphore`

- 12 **Accurate token counting** (optional via 'tiktoken')




**Fast & scalable** async I/O design

# ## How It Works

1. User replies to a message containing text

2. User runs `/summarize`

3. Bot asks for summary style (Short / Bullets / Detailed)

4. The text is split into token-safe chunks

5. Each chunk is summarized using OpenAl

6. Chunk summaries are merged into a final result

7. The summary is cached in SQLite

8. The final summary is sent back to Telegram

# ## APIs Used

# ### Telegram Bot API

- Long polling (no webhook required)

- Inline keyboards for summary mode selection

- Managed via `python-telegram-bot

# ### OpenAl Chat Completion API

- Endpoint: `'POST /v1/chat/completions`

- Used for:

- Chunk-level summarization

- Final summary aggregation

## Requirements

### System Requirements

- Python **3.9+**

- Internet access

- Telegram bot token

- OpenAl API key

# ### Python Dependencies

bash

pip install python-telegram-bot==20.*

pip install httpx

pip install aiosqlite

pip install tiktoken # optional but recommended

# Libraries Used & Reasons

# python-telegram-bot

·Official Telegram wrapper

·Async-first architecture

·Simplifies handlers, commands, and UI components

# httpx

·Async HTTP client

·Ideal for OpenAl API calls

·Cleaner than requests in async environments

# aiosqlite

·Async SQLite access

·Prevents blocking the event loop

·Used for caching summaries

# asyncio

·Core async execution

·Controls concurrency and API request limits

# tiktoken (Optional)

·Accurate token counting for OpenAl models

·Prevents exceeding model context limits

·Falls back to heuristic estimation if unavailable

# hashlib

·Generates stable cache keys

· Ensures identical text + mode combinations map correctly

# Caching Strategy

· A SHA-256 hash of (text + summary mode) is generated

·Results are stored in SQLite

·Repeated requests return instantly without calling OpenAl

·Reduces latency and API costs significantly

## Running the Bot

export TELEGRAMTOKEN="yourtelegramtoken"

export OPENAIAPIKEY="youropenaikey"

python telegramsummarizerbot.py

# Example Use Cases

· Summarizing articles or research papers

· Creating executive summaries

·Bullet-pointing meeting notes

·Educational content digestion

·Chat-based content compression

# Compliance & Best Practices

·Complies with OpenAl API usage guidelines

·Respects token limits

·Async-safe and scalable architecture

·Environment-based configuration

# ·Clean separation of concern

# License

This project is provided as-is for educational and development purposes.

You are responsible for complying with OpenAI and Telegram terms of service.

# Future Improvements (Optional)

·Streaming responses

·User-specific summary preferences

·Multi-language support

·Docker deployment

.Webhook-based Telegram integration
