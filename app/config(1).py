from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    max_text_length: int = 12_000
    max_image_size_mb: int = 10
    ocr_languages: tuple[str, ...] = ("en",)
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()

        telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        openai_key = os.getenv("OPENAI_API_KEY", "").strip()

        missing = []
        if not telegram_token:
            missing.append("TELEGRAM_BOT_TOKEN")
        if not openai_key:
            missing.append("OPENAI_API_KEY")
        if missing:
            raise ValueError(
                "Missing required environment variable(s): "
                + ", ".join(missing)
                + ". Copy .env.example to .env and fill in the values."
            )

        try:
            max_text_length = int(os.getenv("MAX_TEXT_LENGTH", "12000"))
            max_image_size_mb = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
        except ValueError as exc:
            raise ValueError("MAX_TEXT_LENGTH and MAX_IMAGE_SIZE_MB must be integers.") from exc

        if max_text_length < 1:
            raise ValueError("MAX_TEXT_LENGTH must be greater than zero.")
        if max_image_size_mb < 1:
            raise ValueError("MAX_IMAGE_SIZE_MB must be greater than zero.")

        languages = tuple(
            item.strip()
            for item in os.getenv("OCR_LANGUAGES", "en").split(",")
            if item.strip()
        )
        if not languages:
            languages = ("en",)

        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        if log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("LOG_LEVEL must be a valid Python logging level.")

        openai_model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
        if not openai_model:
            openai_model = "gpt-4.1-mini"

        return cls(
            telegram_bot_token=telegram_token,
            openai_api_key=openai_key,
            openai_model=openai_model,
            max_text_length=max_text_length,
            max_image_size_mb=max_image_size_mb,
            ocr_languages=languages,
            log_level=log_level,
        )
