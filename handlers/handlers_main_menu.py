import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
import user_data
import text
import config
import const
from datetime import datetime, timedelta
from logger import logger
from config import dp, bot
import keyboards
import sub

tarif_info = """📚 Продукт: "ОСНОВА"

🗓 Тарифный план: ежемесячная подписка

🚨 Оплачивая подписку, Вы принимаете условия Пользовательского соглашения и Политики конфиденциальности."""


# мои ключи
@dp.message_handler(lambda message: message.text == '🗓 Тарифные планы', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await delete_from_channel(user_id)
    await bot.send_message(chat_id=user_id,
                           text=tarif_info,
                           parse_mode="HTML",
                           reply_markup=keyboards.keyboard_period())
    logger.info(f'user - {user_id} - Тарифные планы')


async def delete_from_channel(user_id):
    sub_info = sub.get_subscription_info(user_id)
    if not sub_info:
        try:
            await bot.ban_chat_member(chat_id=const.channel_id, user_id=user_id)
            logger.info(f'Пользователь {user_id} исключен из канала {const.channel_id}')
        except Exception as e:
            logger.error(f'Ошибка при исключении пользователя: {e}')


@dp.message_handler(lambda message: message.text == '🗃 Моя подписка', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    stop_date = sub.get_subscription_info(user_id)
    await delete_from_channel(user_id)
    if stop_date:
        date_farmated = sub.format_date_string(stop_date)
        txt_my_tarif_info = text.my_tarif_info(date_farmated)
        await bot.send_message(chat_id=user_id,
                               text=txt_my_tarif_info,
                               parse_mode="HTML",
                               reply_markup=keyboards.renewal_sub())
        logger.info(f'user - {user_id} - Моя подписка (до {stop_date})')
    else:
        txt_my_tarif_info = text.my_tarif_info(stop_date)
        await bot.send_message(chat_id=user_id,
                               text=txt_my_tarif_info,
                               parse_mode="HTML",
                               reply_markup=keyboards.keyboard_period())
        logger.info(f'user - {user_id} - Моя подписка (нет подписки)')


@dp.message_handler(lambda message: message.text == '🤝 Поддержка', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await delete_from_channel(user_id)
    answer = f'''🤝 Поддержка

    Написать в поддержку {config.support}'''

    await bot.send_message(chat_id=user_id,
                           text=answer,
                           parse_mode='HTML')
    logger.info(f'user_id - {user_id} - Поддержка')


@dp.message_handler(lambda message: message.text == '👥 Реферальная программа', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await delete_from_channel(user_id)
    count_referrals = user_data.count_referrals(user_id)
    if not count_referrals:
        count_referrals = 0
    user_balance = user_data.get_user_balance_bonus(user_id)
    sub_info = sub.get_subscription_info(user_id)
    if not sub_info:
        txt = text.not_ref_link(count_referrals, user_balance)
        await bot.send_message(chat_id=user_id,
                               text=txt,
                               parse_mode='HTML')
        logger.info(f'user_id - {user_id} - Реферальная программа')
        return
    txt = text.ref_link(user_id, const.bot_name, count_referrals, user_balance)
    await bot.send_message(chat_id=user_id,
                           text=txt,
                           parse_mode='HTML')
    logger.info(f'user_id - {user_id} - Реферальная программа')


@dp.message_handler(lambda message: message.text == 'Отзывы', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await delete_from_channel(user_id)
    txt = f'Перейти к отзывам - https://t.me/osnova_feedbackk'
    await bot.send_message(chat_id=user_id,
                           text=txt,
                           parse_mode='HTML')
    logger.info(f'user_id - {user_id} - Отзывы')


@dp.message_handler(commands=['menu'], state="*")
async def main_menu(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id,
                           text="Главное меню",
                           parse_mode="HTML",
                           reply_markup=keyboards.main_menu())
