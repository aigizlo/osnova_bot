import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
import user_data
import text
import config
from datetime import datetime, timedelta
from logger import logger
from config import dp, bot
import keyboards.keyboards
import sub

tarif_info = """📚 Продукт: "ОСНОВА"

🗓 Тарифный план: ежемесячная подписка

🚨 Оплачивая подписку, Вы принимаете условия Пользовательского соглашения и Политики конфиденциальности."""


# мои ключи
@dp.message_handler(lambda message: message.text == '🗓 Тарифные планы', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    await bot.send_message(chat_id=telegram_id,
                           text=tarif_info,
                           parse_mode="HTML",
                           reply_markup=keyboards.keyboards.keyboard_period())


@dp.message_handler(lambda message: message.text == '🗃 Моя подписка', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    stop_date = sub.get_subscription_info(telegram_id)
    if stop_date:
        date_farmated = sub.format_date_string(stop_date)
        txt_my_tarif_info = sub.my_tarif_info(date_farmated)
        await bot.send_message(chat_id=telegram_id,
                               text=txt_my_tarif_info,
                               parse_mode="HTML")
    else:
        txt_my_tarif_info = sub.my_tarif_info(stop_date)
        await bot.send_message(chat_id=telegram_id,
                               text=txt_my_tarif_info,
                               parse_mode="HTML",
                               reply_markup=keyboards.keyboards.keyboard_period())


@dp.message_handler(lambda message: message.text == '🤝 Поддержка', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id

    answer = f'''🤝 Поддержка

    Написать в поддержку {config.support}'''

    await bot.send_message(chat_id=telegram_id,
                           text=answer,
                           parse_mode='HTML')


@dp.message_handler(lambda message: message.text == '👥 Реферальная программа', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    count_referrals = user_data.count_referrals(telegram_id)
    if not count_referrals:
        count_referrals = 0
    user_balance = user_data.get_user_balance_bonus(telegram_id)

    sub_info = sub.get_subscription_info(telegram_id)

    if not sub_info:
        txt = text.not_ref_link(count_referrals, user_balance)
        await bot.send_message(chat_id=telegram_id,
                               text=txt,
                               parse_mode='HTML')
        return

    txt = text.ref_link(telegram_id, config.bot_name, count_referrals, user_balance)

    await bot.send_message(chat_id=telegram_id,
                           text=txt,
                           parse_mode='HTML')
