from telegram.ext import (
    ContextTypes,
)
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from config.states import MAIN_MENU

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("создать презентацию", callback_data='create_presentation')],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query: 
        query = update.callback_query
        await query.answer()

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=".", reply_markup=markup
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=".", reply_markup=markup
        )

    return MAIN_MENU
