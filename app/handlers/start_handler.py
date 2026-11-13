from telegram import Update
from telegram.ext import ContextTypes


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        "سلام! به LexiBot خوش آمدی 📚\n\n"
        "یک کلمه، عبارت یا متن انگلیسی بفرست تا معنی یا ترجمه‌اش را ارائه کنم.\n"
        "همچنین می‌توانی از متن انگلیسی عکس بفرستی."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    if update.message is None:
        return

    await update.message.reply_text(
        "راهنمای LexiBot\n"
        "• ارسال کلمه: معنی فارسی و انگلیسی، نقش دستوری، مترادف و متضاد\n"
        "• ارسال عبارت: معنی و کاربرد عبارت\n"
        "• ارسال متن: ترجمه کامل متن به فارسی\n"
        "• ارسال عکس: استخراج متن انگلیسی و پردازش آن\n\n"
        "برای شروع /start را بفرست."
    )
