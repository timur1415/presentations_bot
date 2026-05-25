import os

from telegram.ext import (
    ContextTypes,
)
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup
)

from config.states import DESCRIPTION, TOPIC, FINISH_PROMPT, SEND_PRESENTTION

from openai import OpenAI

from config.config import CHAT_GPT_TOKEN

from main_work.create_presentation import create_presentation

async def slide(update: Update, context: ContextTypes):
    keyboard = [['3-5'], ['10-15'], ['20+']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выбери, сколько слайдов должно быть в презентации.",
        reply_markup=markup
    )

    return TOPIC

async def topic(update: Update, context: ContextTypes):
    context.user_data['slide'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Укажи тему презентации, которую хочешь создать."
    )
    return DESCRIPTION


async def description(update: Update, context: ContextTypes):
    context.user_data['topic'] = update.effective_message.text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Опиши презентацию: стиль, цветовую гамму, желаемый дизайн и, если хочешь, добавь примерный текст или идеи для слайдов."
    )
    return FINISH_PROMPT

async def finish_prompt(update: Update, context: ContextTypes):
    keyboard = [['далее']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    description = update.effective_message.text

    prompt_creator = f"""
Ты профессиональный дизайнер презентаций и prompt engineer.

На основе данных пользователя создай готовую структуру презентации.

ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:

Тема:
{context.user_data['topic']}

Количество слайдов:
{context.user_data['slide']}

Пожелания:
{description}

ЗАДАЧА:

1. Подбери уникальный визуальный стиль презентации под тему.
2. Подбери:
- background_color
- title_color
- text_color
- accent_color

Цвета возвращай строго в HEX.

После этого создай полный контент презентации.

ТРЕБОВАНИЯ:

- современный premium дизайн
- единый визуальный стиль
- минимализм
- много воздуха
- без перегруженности
- красивые заголовки
- краткий и информативный текст
- 3–5 коротких пунктов на каждом слайде
- не более 6–10 слов в пункте
- каждый слайд уникальный по смыслу
- одинаковый стиль на всей презентации

ФОРМАТ ОТВЕТА СТРОГО:

STYLE:
background_color: #HEX
title_color: #HEX
text_color: #HEX
accent_color: #HEX

SLIDES:

TITLE: Заголовок
TEXT:
- пункт
- пункт
- пункт

TITLE: Заголовок
TEXT:
- пункт
- пункт
- пункт

TITLE: Заголовок
TEXT:
- пункт
- пункт
- пункт

ВАЖНО:

- без markdown
- без пояснений
- без текста до блока STYLE
- после STYLE сразу SLIDES
- строго соблюдать формат
- вернуть только готовый результат
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
    context.user_data['ai_prompt'] = response.choices[0].message.content

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="вот подробный план презентации", reply_markup=markup
    )

    return SEND_PRESENTTION


async def send_presentation(update: Update, context: ContextTypes):
    keyboard = [
    [InlineKeyboardButton("Создать ещё", callback_data="new_presentation")],
    [InlineKeyboardButton("Главное меню", callback_data="menu")]
]

    markup = InlineKeyboardMarkup(keyboard)


    presentation_prompt = f"""
Создай JSON презентации.

Тема:
{context.user_data["topic"]}

Количество слайдов:
{context.user_data["slide"]}

Пожелания:
{context.user_data["ai_prompt"]}

Верни строго JSON:

{{
  "background_color": "#HEX",
  "title_color": "#HEX",
  "text_color": "#HEX",
  "accent_color": "#HEX",
  "slides": [
    {{
      "layout": "title",
      "title": "...",
      "bullets": ["...", "...", "..."]
    }}
  ]
}}

ПРАВИЛА:
- Только JSON
- Без markdown
- Без ```json
- Цвета только HEX
- 3–5 bullets
- bullets короткие
- каждый слайд визуально отличается
- стиль premium minimal
"""

    client = OpenAI(api_key=CHAT_GPT_TOKEN)

    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "system",
                "content": presentation_prompt
            }
        ]
    )

    response_text = response.choices[0].message.content

    file_name = create_presentation(
        topic=context.user_data["topic"],
        slides_text=response_text,
        style_text=""
    )

    with open(file_name, "rb") as file:
        await context.bot.send_document(
            chat_id=update.effective_chat.id,
            document=file,
            filename=file_name,
            reply_markup=markup
        )

    os.remove(file_name)