import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    filters,
    ConversationHandler,
    PicklePersistence,
    CallbackQueryHandler,
    MessageHandler
)
from config.config import TOKEN

from start import start

from config.states import MAIN_MENU, TOPIC, DESCRIPTION, FINISH, FINISH_PROMPT

from main_work.create_presentation import topic, description, finish_prompt, slide

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    persistence = PicklePersistence(filepath="presentations_bot")
    application = ApplicationBuilder().token(TOKEN).persistence(persistence).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU:[
                CallbackQueryHandler(slide, pattern='^create_presentation$'),
            ],
        TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, topic)],
        DESCRIPTION:[MessageHandler(filters.TEXT & ~filters.COMMAND, description)],
        FINISH_PROMPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_prompt),]
        },
        fallbacks=[CommandHandler("start", start)],
        name="presentations_bot",
        persistent=True,
    )

    application.add_handler(conv_handler)

    application.run_polling()