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
    query = update.callback_query
    await query.answer()
    keyboard = [['3-5'], ['6-10']]
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
    text=(
    "Максимально подробно опиши презентацию — это очень важно для качественного результата.\n\n"
    "Укажи стиль, цветовую гамму, желаемый дизайн, атмосферу, предпочтительные шрифты, "
    "анимации, формат слайдов и любые детали, которые помогут точнее передать твоё видение.\n\n"
    "Также можешь добавить примерный текст для слайдов, структуру презентации, ключевые идеи, "
    "пожелания по визуалам, изображениям, иконкам или графикам. "
    "Чем подробнее будет описание, тем лучше получится итоговая презентация."
    )
    )
    return FINISH_PROMPT

async def finish_prompt(update: Update, context: ContextTypes):
    keyboard = [['далее']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    description = update.effective_message.text

    prompt_builder_prompt = f"""
Ты — AI Presentation Prompt Architect.

Твоя задача — создать идеальный prompt для второй AI-модели, которая будет генерировать JSON презентации.

ВАЖНО:

Ты НЕ создаёшь презентацию.
Ты НЕ создаёшь JSON.
Ты НЕ пишешь текст слайдов.

Ты создаёшь только prompt для следующей модели.


ВХОДНЫЕ ДАННЫЕ:

Тема презентации:
{context.user_data["topic"]}

Количество слайдов:
{context.user_data["slide"]}

Описание пользователя:
{description}


ТВОЯ ЗАДАЧА:

Проанализируй все входные данные.

На основе них создай максимально качественный production-ready prompt для второй AI-модели.


Главное правило:

Максимально опирайся на описание пользователя.

Если пользователь написал:

— стиль
— настроение
— цветовую палитру
— количество текста
— минимализм
— корпоративный стиль
— академический стиль
— современный стиль
— наличие изображений
— подробно / кратко
— визуальные пожелания

то это имеет абсолютный приоритет над дефолтными настройками.



Если пользователь НЕ уточнил деталей — используй дефолтные правила ниже.



ДЕФОЛТНЫЕ ПРАВИЛА:

— стиль: premium minimal modern
— презентация визуальная
— минималистичная
— современная
— аккуратная
— текст краткий
— 6–8 bullets на слайд
— каждый bullet короткий
— 1 мысль = 1 bullet
— без длинных абзацев
— без перегруженных текстовых блоков
— layouts разнообразные
— одинаковые layouts подряд не использовать
— высокий визуальный контраст
— readability выше дизайна
— декор только фоновый
— фигуры не пересекаются с текстом
— карточки использовать редко
— если карточка ухудшает читаемость — не использовать



ПРАВИЛА ДЛЯ ТЕКСТА:

Если пользователь просит кратко:

— 4–6 bullets

Если пользователь ничего не указал:

— 6–8 bullets

Если пользователь просит подробно:

— 8–12 bullets
или более развёрнутые bullets


Каждый bullet:

— короткий
— ёмкий
— легко читается с экрана



ПРАВИЛА ВИЗУАЛА:

Обязательно опиши для второй модели:

— стиль
— настроение
— text density
— количество bullets
— layouts
— цветовую палитру
— safe area
— правила контраста
— правила работы с карточками
— правила читаемости
— правила разнообразия между слайдами



ФОРМАТ ОТВЕТА:

Верни ТОЛЬКО готовый prompt для второй модели.

Без пояснений.

Без markdown.

Без `.

Только чистый prompt.
"""
    client = OpenAI(api_key=CHAT_GPT_TOKEN)
    response = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "system",
                "content": f"{prompt_builder_prompt}"
            }
        ]
    )
    context.user_data['ai_prompt'] = response.choices[0].message.content

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Ваша презентация почти готова\n\nЕсли преза получется не очень то вы можете отправить боту <<ещё>>", reply_markup=markup
    )

    return SEND_PRESENTTION


async def send_presentation(update: Update, context: ContextTypes):
    keyboard = [
    [InlineKeyboardButton("Создать ещё", callback_data="new_presentation")],
    [InlineKeyboardButton("Главное меню", callback_data="menu")]
]

    markup = InlineKeyboardMarkup(keyboard)

    presentation_prompt = f"""
{context.user_data["ai_prompt"]}

ВАЖНО:

Верни результат строго в JSON формате.

Обязательно используй именно эту структуру:

{{
  "background_color": "#HEX",
  "title_color": "#HEX",
  "text_color": "#HEX",
  "accent_color": "#HEX",
  "slides": [
    {{
      "layout": "title",
      "title": "...",
      "bullets": [
        "...",
        "..."
      ]
    }}
  ]
}}

ОБЯЗАТЕЛЬНО:

— background_color обязателен
— title_color обязателен
— text_color обязателен
— accent_color обязателен
— slides обязателен

Только JSON.

Без markdown.

Без ```json

Без пояснений.

Без текста до JSON.

Без текста после JSON.
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