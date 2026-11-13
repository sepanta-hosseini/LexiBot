import logging

from telegram import Update
from telegram.ext import ContextTypes

from app.services.ai_service import AIService, AIServiceError
from app.utils.text_utils import format_ai_response, split_message

logger = logging.getLogger(__name__)


async def handle_text(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None or not update.message.text:
        return

    ai_service: AIService = context.application.bot_data["ai_service"]
    status_message = await update.message.reply_text("در حال بررسی متن... ⏳")

    try:
        result = await ai_service.analyze(update.message.text)
        response = format_ai_response(result)
        await status_message.delete()
        for chunk in split_message(response):
            await update.message.reply_text(chunk)
    except AIServiceError as exc:
        logger.warning("Text analysis could not be completed: %s", exc)
        await status_message.edit_text(str(exc))
    except Exception:
        logger.exception("Unexpected text handler error.")
        await status_message.edit_text(
            "هنگام پردازش پیام مشکلی پیش آمد. لطفاً دوباره تلاش کن."
        )
