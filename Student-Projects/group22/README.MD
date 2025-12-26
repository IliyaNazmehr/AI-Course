## 🧩 Team Members
- Ali Baradarcherli 40010130117343
- Hossein Jafari 40010130117344
- Arshia mashayekhi 40110130117266

## 🎯 Project Title
Telegram OCR BOT

## 🧠 Summary
This is a Telegram Bot that extracts text from images using pytesseract (Tesseract OCR) and the Python Telegram API. Users can send an image to the bot, and it will respond with the extracted text from the image.
[USE IT](https://t.me/test_ansfd123nasdfbot)

## 🚀 How to Run
1. Clone the repository.
2. Create a Telegram bot with **BotFather** and copy the bot token.
3. Copy `env_example` to `.env` and update the values (do **not** commit `.env`).
4. Build and run the bot with Docker Compose: `docker compose up --build -d`.
5. Check logs and test the bot in Telegram.

---

## Requirements

* Docker (latest stable release recommended)
* Docker Compose
* A Telegram account (to create a bot via BotFather)


## 1) Clone the repository

Run the standard `git` clone command (adjust the URL if you use SSH):

```bash
git clone https://github.com/IliyaNazmehr/AI-Course
cd AI-Course/Student-Projects/group22/
```

---

## 2) Create a Telegram bot and obtain the token (BotFather)

1. Open the Telegram app and search for `@BotFather`.
2. Send `/newbot` and follow the prompts; choose a name and a username (must end with `bot`).
3. BotFather will reply with a token in this format: `1234567890:ABC...`.
4. Copy that token — you will paste it into your `.env`.

> Keep the token secret. If the token is ever exposed, revoke it with BotFather and generate a new one.

---

## 3) Prepare environment variables

There is an `env_example` file in the repo. Copy it to create your local `.env` and edit the values.

```bash
cp env_example .env
# then open .env with your editor and paste your BOT_TOKEN
# e.g. BOT_TOKEN=1234567890:ABCDEFyourtoken
```

**Important values** (example names; follow the variables defined in your `env_example`):

* `BOT_TOKEN` — the token you obtained from BotFather.
* `TESSDATA_PREFIX` — path inside the container where Tesseract language data lives (default used by the Dockerfile is `/usr/share/tesseract-ocr/5`).

Do **not** commit `.env`; add it to `.gitignore` (see below).

---

## 4) Build and run with Docker Compose

From the repository root run:

```bash
docker compose up --build -d
```

This command will build the Docker image (using the `Dockerfile`) and start the container declared in `docker-compose.yml`.

To follow logs:

```bash
docker compose logs -f
```

To stop the service:

```bash
docker compose down
```

---

## 5) Test the bot

1. Open Telegram and start a chat with your bot (search for the username you created).
2. Send an image that contains text. The bot should reply with extracted text.
3. If it does not work, check container logs and the `bot.py` implementation for any errors.

Useful commands while debugging:

```bash
# view last 200 lines of logs
docker compose logs --tail=200
# follow logs continuously
docker compose logs -f
```

---

## Troubleshooting tips

* `Unauthorized` errors from Telegram indicate an incorrect or revoked token.
* `tesseract: command not found` means the runtime image does not have Tesseract installed — check your Dockerfile.
* If OCR quality is poor, try preprocessing images (increase DPI, denoise, binarize) and experiment with `--psm` options.

---

