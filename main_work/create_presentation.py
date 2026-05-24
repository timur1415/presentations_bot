from telegram.ext import (
    ContextTypes,
)
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)

from config.states import DESCRIPTION, TOPIC, FINISH_PROMPT, AI_PROMPT, FINISH

from openai import OpenAI

from config.config import CHAT_GPT_TOKEN

async def slide(update: Update, context: ContextTypes):
    keyboard = [['3-5'], ['10-15'], ['20+']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="сколько слайдов?", reply_markup=markup
    )

    return TOPIC

async def topic(update: Update, context: ContextTypes):
    context.user_data['slide'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="на какую тему делать презентацию"
    )
    return DESCRIPTION


async def description(update: Update, context: ContextTypes):
    context.user_data['topic'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="опиши презинтацию. как хочешь чтобы она выглядела тема цвета и возможно текст(заготовки для слайдов)"
    )
    return FINISH_PROMPT

async def finish_prompt(update: Update, context: ContextTypes):
    description = update.effective_message.text

    prompt_creator = f"""

Ты профессиональный prompt engineer для AI-презентаций.

Твоя задача:

создать ИДЕАЛЬНЫЙ PROMPT для генерации презентации.

ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:

Тема:

{context.user_data['topic']}

Количество слайдов:

{context.user_data['slide']}

Пожелания:

{description}

Создай ОЧЕНЬ подробный prompt для AI-модели,

которая будет создавать презентацию.

Prompt должен:

- объяснять стиль презентации

- объяснять структуру слайдов

- объяснять визуальный стиль

- задавать профессиональный уровень

- запрещать длинные тексты

- требовать современный дизайн

- требовать уникальность слайдов

- требовать красивые заголовки

- требовать краткость

- требовать информативность

- требовать premium качество

Prompt должен быть:

- максимально подробным

- профессиональным

- готовым для production использования

Верни ТОЛЬКО готовый prompt.

Без пояснений.

максимум 4000 символов

"""
    client = OpenAI(api_key=CHAT_GPT_TOKEN)
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "system",
                "content": f"{prompt_creator}"
            }
        ]
    )
    ai_prompt = response.choices[0].message.content
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ai_prompt
    )
