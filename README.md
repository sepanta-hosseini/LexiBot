# LexiBot 🤖📚

LexiBot is an AI-powered Telegram bot for English vocabulary and text translation. Users can send an English word, phrase, full text, or an image containing English text.

## Features

- Word definitions in English and Persian
- Part of speech
- Synonyms and antonyms when they naturally exist
- Phrase and idiom explanations
- Full-text Persian translation
- Image text extraction with EasyOCR
- Async Telegram and OpenAI requests
- Input-size limits and basic error handling

## Tech stack

- Python 3.11+
- python-telegram-bot
- OpenAI Python SDK
- EasyOCR (optional image dependency)
- Pydantic
- python-dotenv
- pytest

## Project structure

```text
LexiBot/
├── app/
│   ├── handlers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   ├── config.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── requirements-ocr.txt
```

## Setup (Windows PowerShell)

1. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

2. Install base dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. For image/OCR support, install the optional OCR dependencies:

   ```powershell
   pip install -r requirements-ocr.txt
   ```

   EasyOCR also installs PyTorch dependencies. On some Windows machines, PyTorch installation may require choosing a compatible CPU/CUDA command from the official PyTorch installation selector.

4. Copy `.env.example` to `.env` and add your Telegram bot token and OpenAI API key.

   ```powershell
   Copy-Item .env.example .env
   ```

5. Start the bot from the project root:

   ```powershell
   python -m app.main
   ```

6. Open your bot in Telegram and send `/start`.

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Yes | - | Token from BotFather |
| `OPENAI_API_KEY` | Yes | - | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4.1-mini` | Model used for analysis |
| `MAX_TEXT_LENGTH` | No | `12000` | Maximum input characters |
| `MAX_IMAGE_SIZE_MB` | No | `10` | Maximum image size |
| `OCR_LANGUAGES` | No | `en` | Comma-separated EasyOCR languages |
| `LOG_LEVEL` | No | `INFO` | Python logging level |

## Run tests

```powershell
pytest -q
```

The tests use mocked AI responses and do not call Telegram or OpenAI.

## Security notes

- Never commit `.env` or publish API keys.
- Rotate a token immediately if it is accidentally exposed.
- API usage may incur charges.
- Do not send sensitive personal information to the bot.
- OCR is optional and is initialized only when the first image is received.

## Current limitations

- The initial OCR configuration is English-only.
- The bot uses Telegram long polling and is intended for a single running instance.
- There is no database or user history yet.
- AI output should be treated as a learning aid and may occasionally need verification.
