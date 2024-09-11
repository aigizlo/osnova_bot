from aiogram import types
import const


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("menu", "Главное меню"),
        ]
    )

# кнопка Назад
def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button1 = types.KeyboardButton('🗓 Тарифные планы')
    button2 = types.KeyboardButton('🗃 Моя подписка')
    button3 = types.KeyboardButton('Отзывы')
    button4 = types.KeyboardButton('🤝 Поддержка')
    button5 = types.KeyboardButton('👥 Реферальная программа')

    # Добавляем первый ряд с двумя кнопками
    keyboard.row(button1, button2)

    # Добавляем второй ряд с одной кнопкой на всю ширину
    keyboard.row(button3)

    # Добавляем третий ряд с двумя кнопками
    keyboard.row(button4, button5)

    return keyboard


def keyboard_period():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("1 месяц - 30 дней - 15 USD", callback_data=f"period:1"),
        types.InlineKeyboardButton("3 месяца - 90 дней - 40 USD", callback_data=f"period:3"),
        types.InlineKeyboardButton("12 месяцев - 365 дней - 150 USD", callback_data=f"period:12")
    )
    return keyboard


def accept_button():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("🟢 ПРИНИМАЮ ПРАВИЛА 🟢", callback_data=f"accept_rules"),
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


def go_to_pay():
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
        types.InlineKeyboardButton("""✅ Канал "ОСНОВА" Подписаться""", url=const.tg_channel_link),
        types.InlineKeyboardButton("🔁 Проверить подписку", callback_data="subscribe_check"),

    )
    return keyboard


def join_chat():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("""Чат «ФУНДАМЕНТАЛИСТЫ - вступить""", url=const.tg_chat)

    )
    return keyboard


def renewal_sub():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("""✅Продлить подписку""", callback_data='renewal_sub')
    )
    return keyboard
