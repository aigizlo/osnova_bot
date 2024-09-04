from aiogram import types
from config import tg_channel_link, article
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import one_month, three_month, one_year


# кнопка Назад
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('🗓 Тарифные планы')
    button3 = types.KeyboardButton('🗃 Моя подписка')
    button2 = types.KeyboardButton('👥 Реферальная программа')
    button4 = types.KeyboardButton('🤝 Поддержка')
    keyboard.add(button1, button2, button3, button4)

    return keyboard

def keyboard_period():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("1 месяц - 30 дней - 15 USD", callback_data=f"period:1"),
        types.InlineKeyboardButton("3 месяца - 90 дней - 40 USD", callback_data=f"period:3"),
        types.InlineKeyboardButton("12 месяцев - 365 дней - 150 USD", callback_data=f"period:12")
    )
    return keyboard


def select_pay_method():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("💳 Оплатить", callback_data="go_pay"),
        types.InlineKeyboardButton("🎁 Применить промокод", callback_data="apply_promo"),
        types.InlineKeyboardButton("🎁 Подарить подписку", callback_data="gift_subscription"),
        types.InlineKeyboardButton("⬅️ Назад", callback_data="go_back_to_main")
    )
    return keyboard

def go_pay():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Перейти к оплате", callback_data="select_pay_method"),
        types.InlineKeyboardButton("⬅️ Назад", callback_data="go_back"),
    )
    return keyboard

def select_card_or_usdt():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Оплатить картой", callback_data=f"card_pay"),
        types.InlineKeyboardButton("USTD (trc2-)", callback_data=f"usdt_pay"),
        types.InlineKeyboardButton("⬅️ Назад", callback_data=f"go_back_to_main"),
    )
    return keyboard

def back_to_main_menu():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("⬅️ Назад", callback_data="go_back_to_main")
    )
    return keyboard


# клавиатура где пользователю предлагаем подписаться на канал
def subscribe():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("""✅ Канал "ОСНОВА" Подписаться""", url=tg_channel_link),
        types.InlineKeyboardButton("🔁 Проверить подписку", callback_data="subscribe_check"),

    )
    return keyboard

def subscribe():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("""✅Принимаю правила""", url=tg_channel_link),

    )
    return keyboard

