import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7633150137:AAELwitp1R9ZB7V4RDrwWGyz4O48VDXXumA"

# Укажите здесь ID администратора, чьи сообщения бот не должен проверять
ADMIN_ID = 5146454740  # Замените на реальный ID администратора

# Расширенный список корневых частей слов для фильтрации спама
SPAM_KEYWORDS = [
    "заработ",        # покроет: заработок, заработка, заработком и т.д.
    "доход",          # доход, доходы, доходом и т.д.
    "реклам",         # реклама, рекламировать, рекламу и т.д.
    "партнерк",       # партнерка, партнёрка, партнерки и т.д.
    "финансовая свобода",
    "быстрый заработок",
    "пассивный доход",
    "криптовалют",
    "инвестиц",
    # Добавляйте другие ключевые слова по необходимости
]

async def anti_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляем сообщение, если оно содержит спам-слова, за исключением сообщений администратора."""
    # Если отправитель является администратором, пропускаем проверку
    if update.message and update.message.from_user and update.message.from_user.id == ADMIN_ID:
        return

    if update.message and update.message.text:
        message_text = update.message.text.lower()
        if any(keyword in message_text for keyword in SPAM_KEYWORDS):
            try:
                await update.message.delete()
                logger.info(
                    f"Удалено спам-сообщение от {update.message.from_user.full_name}: {update.message.text}"
                )
            except Exception as e:
                logger.error(f"Ошибка при удалении сообщения: {e}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    # Обработчик для всех текстовых сообщений, кроме команд
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, anti_spam))
    application.run_polling()

if __name__ == '__main__':
    main()
