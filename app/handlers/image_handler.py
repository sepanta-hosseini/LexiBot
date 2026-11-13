import logging
import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from app.services.ai_service import AIService, AIServiceError
from app.services.ocr_service import OCRService, OCRServiceError
from app.utils.text_utils import format_ai_response, split_message

logger = logging.getLogger(__name__)


async def handle_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None or not update.message.photo:
        return

    settings = context.application.bot_data["settings"]
    ocr_service: OCRService = context.application.bot_data["ocr_service"]
    ai_service: AIService = context.application.bot_data["ai_service"]

    photo = update.message.photo[-1]
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    if photo.file_size and photo.file_size > max_bytes:
        await update.message.reply_text(
            f"حجم عکس بیش از حد مجاز است. حداکثر حجم: {settings.max_image_size_mb} MB"
        )
        return

    status_message = await update.message.reply_text(
        "عکس دریافت شد. در حال استخراج متن... 🖼️"
    )

    try:
        telegram_file = await context.bot.get_file(photo.file_id)
        with tempfile.TemporaryDirectory(prefix="lexibot_") as temp_dir:
            image_path = Path(temp_dir) / "telegram_image.jpg"
            await telegram_file.download_to_drive(custom_path=str(image_path))
            extracted_text = await ocr_service.extract_text(str(image_path))

        result = await ai_service.analyze(extracted_text)
        response = "📝 متن استخراج‌شده از تصویر:\n" + extracted_text
        response += "\n\n" + format_ai_response(result)

        await status_message.delete()
        for chunk in split_message(response):
            await update.message.reply_text(chunk)

    except OCRServiceError as exc:
        logger.warning("Image OCR failed: %s", exc)
        await status_message.edit_text(str(exc))
    except AIServiceError as exc:
        logger.warning("AI analysis of image text failed: %s", exc)
        await status_message.edit_text(str(exc))
    except Exception:
        logger.exception("Unexpected image handler error.")
        await status_message.edit_text(
            "هنگام پردازش تصویر مشکلی پیش آمد. لطفاً تصویر دیگری امتحان کن."
        )
