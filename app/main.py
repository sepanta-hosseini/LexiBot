import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
)

from app.config import Settings
from app.handlers.image_handler import handle_image
from app.handlers.start_handler import help_command, start_command
from app.handlers.text_handler import handle_text
from app.services.ai_service import AIService
from app.services.ocr_service import OCRService


async def error_handler(update: object, context) -> None:
    error = context.error
    logger = logging.getLogger(__name__)
    if error is not None:
        logger.error(
            "Unhandled Telegram application error.",
            exc_info=(type(error), error, error.__traceback__),
        )
    else:
        logger.error("Unhandled Telegram application error without exception details.")
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "یک خطای پیش‌بینی‌نشده رخ داد. لطفاً کمی بعد دوباره تلاش کن."
            )
        except Exception:
            logging.getLogger(__name__).exception(
                "Could not send error notification to the user."
            )


def build_application(settings: Settings) -> Application:
    ai_service = AIService(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        max_text_length=settings.max_text_length,
    )
    ocr_service = OCRService(languages=settings.ocr_languages)

    application = Application.builder().token(settings.telegram_bot_token).build()
    application.bot_data["settings"] = settings
    application.bot_data["ai_service"] = ai_service
    application.bot_data["ocr_service"] = ocr_service

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text)
    )
    application.add_error_handler(error_handler)

    return application


def main() -> None:
    settings = Settings.from_env()
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    application = build_application(settings)
    logging.getLogger(__name__).info("LexiBot is starting.")
    application.run_polling()


if __name__ == "__main__":
    main()
