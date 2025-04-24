
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Напиши команду /date в формате дд.мм.гггг, чтобы узнать крайний срок возврата.")

async def date_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) != 1:
            raise ValueError("Пример: /date 23.04.2025")
        date_str = context.args[0]
        operation_date = datetime.strptime(date_str, "%d.%m.%Y")
        statement_end = operation_date + timedelta(days=30)
        repayment_deadline = statement_end + timedelta(days=25)

        reply = (
            f"Перевод сделан: {operation_date.strftime('%d %B %Y')}\n"
            f"Расчётный период до: {statement_end.strftime('%d %B %Y')}\n"
            f"Крайний срок возврата: {repayment_deadline.strftime('%d %B %Y')}"
        )
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("date", date_handler))
    app.run_polling()
