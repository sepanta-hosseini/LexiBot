import pytest

from app.config import Settings


def test_settings_load_from_environment(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "telegram-test-token")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test-key")
    monkeypatch.setenv("OCR_LANGUAGES", "en,fa")
    settings = Settings.from_env()
    assert settings.telegram_bot_token == "telegram-test-token"
    assert settings.openai_api_key == "openai-test-key"
    assert settings.ocr_languages == ("en", "fa")
    assert settings.openai_model == "gpt-4.1-mini"


def test_settings_reject_missing_secrets(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="TELEGRAM_BOT_TOKEN, OPENAI_API_KEY"):
        Settings.from_env()


def test_settings_reject_non_positive_limits(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "telegram-test-token")
    monkeypatch.setenv("OPENAI_API_KEY", "openai-test-key")
    monkeypatch.setenv("MAX_TEXT_LENGTH", "0")
    with pytest.raises(ValueError, match="MAX_TEXT_LENGTH"):
        Settings.from_env()
