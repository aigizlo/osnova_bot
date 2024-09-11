# -*- coding: utf-8 -*-

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("menu", "Главное меню"),
        ]
    )


adminpanelmenu = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='С фото 🏞'),
            KeyboardButton(text='С видео 🎥')
        ],
        [
            KeyboardButton(text="Пропустить ➡️")
        ]
    ]
)

adminpanelcontinue = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='продолжить ➡️')
        ]
    ]
)

lang_buttons = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='ru'),
            KeyboardButton(text='en')
        ]
    ]
)


startposting = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подтвердить',callback_data='startposting'),
            InlineKeyboardButton(text='Отменить',callback_data='cancelposting')
        ]
    ]
)

select_users = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Всем'),
            KeyboardButton(text='С подпиской'),
            KeyboardButton(text='Без подписки')
        ]
    ]
)

dalee = ReplyKeyboardMarkup(
    row_width=1,
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Далее'),
        ]
    ]
)