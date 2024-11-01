#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aiogram.utils.exceptions import MigrateToChat, BadRequest, ChatNotFound
import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
import user_data
import text
import config
import const
from datetime import datetime, timedelta
from logger import logger
from config import dp, bot, url_politic_conf, url_polz_solah
import keyboards
import sub

tarif_info = f"""📚 Продукт: "ОСНОВА"

🗓 Тарифный план: ежемесячная подписка

🚨 Оплачивая подписку, Вы принимаете условия <a href="{url_polz_solah}">Пользовательского соглашения</a> и <a href="{url_politic_conf}">Политики конфиденциальности</a>"""


@dp.message_handler(lambda message: message.text == '🗓 Тарифные планы', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    await delete_from_channel(user_id)
    await bot.send_message(chat_id=user_id,
                           text=tarif_info,
                           parse_mode="HTML",
                           disable_web_page_preview=True,
                           reply_markup=keyboards.keyboard_period())
    logger.info(f'user - {user_id} - Тарифные планы')


@dp.message_handler(lambda message: message.text == '🗃 Моя подписка', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    stop_date = sub.get_subscription_info(user_id)
    member_channel = await bot.get_chat_member(chat_id=const.channel_id, user_id=user_id)
    member_chat = await bot.get_chat_member(chat_id=const.chat_id, user_id=user_id)

    if member_channel.status == 'kicked':
        await bot.unban_chat_member(chat_id=const.channel_id, user_id=user_id)
        logger.info(f"Пользователь  {user_id} разбанен в канане")

    if member_chat.status == 'kicked':
        await bot.unban_chat_member(chat_id=const.chat_id, user_id=user_id)
        logger.info(f"Пользователь  {user_id} разбанен в чате")

    await delete_from_channel(user_id)
    if stop_date:
        date_farmated = sub.format_date_string(stop_date)
        txt_my_tarif_info = text.my_tarif_info(date_farmated)
        await bot.send_message(chat_id=user_id,
                               text=txt_my_tarif_info,
                               parse_mode="HTML",
                               disable_web_page_preview=True,
                               reply_markup=keyboards.renewal_sub())
        logger.info(f'user - {user_id} - Моя подписка (до {stop_date})')
    else:
        txt_my_tarif_info = text.my_tarif_info(stop_date)
        await bot.send_message(chat_id=user_id,
                               text=txt_my_tarif_info,
                               parse_mode="HTML",
                               disable_web_page_preview=True,
                               reply_markup=keyboards.keyboard_period()),
        logger.info(f'user - {user_id} - Моя подписка (нет подписки)')


@dp.message_handler(lambda message: message.text == '🤝 Поддержка', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    await delete_from_channel(user_id)
    answer = f'''🤝 Поддержка

    Написать в поддержку {config.support}'''

    await bot.send_message(chat_id=user_id,
                           text=answer,
                           parse_mode='HTML',
                           reply_markup=keyboards.main_menu())
    logger.info(f'user_id - {user_id} - Поддержка')


@dp.message_handler(lambda message: message.text == '👥 Реферальная программа', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):


    user_id = message.from_user.id
    await delete_from_channel(user_id)
    count_referrals = user_data.count_referrals(user_id)
    if not count_referrals:
        count_referrals = 0
    user_balance = user_data.get_user_balance_bonus(user_id)
    txt = text.ref_link(user_id, const.bot_name, count_referrals, user_balance)
    if user_balance >= 50:
        await bot.send_message(chat_id=user_id,
                               text=txt,
                               parse_mode='HTML',
                               reply_markup=keyboards.withdraw())
    else:
        await bot.send_message(chat_id=user_id,
                               text=txt,
                               parse_mode='HTML',
                               reply_markup=keyboards.main_menu())

    logger.info(f'user_id - {user_id} - Реферальная программа')


@dp.message_handler(lambda message: message.text == 'Отзывы', state='*')
async def my_keys_command(message: types.Message, state: FSMContext):

    user_id = message.from_user.id
    await delete_from_channel(user_id)
    txt = f'Перейти к отзывам - https://t.me/osnova_feedbackk'
    await bot.send_message(chat_id=user_id,
                           text=txt,
                           parse_mode='HTML',
                           reply_markup=keyboards.main_menu())
    logger.info(f'user_id - {user_id} - Отзывы')


@dp.message_handler(commands=['menu'], state="*")
async def main_menu(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(chat_id=user_id,
                           text="Главное меню",
                           parse_mode="HTML",
                           reply_markup=keyboards.main_menu())


async def delete_from_channel(user_id):
    sub_info = sub.get_subscription_info(user_id)
    if not sub_info:
        async def try_ban(chat_id, user_id, chat_type):
            try:
                member_chat = await bot.get_chat_member(chat_id=const.chat_id, user_id=user_id)
                logger.info(f'member_chat {member_chat.status}')
                if member_chat.status != 'kicked':
                    await bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
                    logger.info(f'Пользователь {user_id} исключен из {chat_type} {chat_id}')

            except MigrateToChat as e:
                new_chat_id = e.migrate_to_chat_id
                logger.info(f"{chat_type.capitalize()} был преобразован в супергруппу. Новый ID: {new_chat_id}")
                await try_ban(new_chat_id, user_id, chat_type)
            except BadRequest as e:
                if "user is an administrator" in str(e).lower():
                    logger.error(f"Невозможно исключить администратора из {chat_type} {chat_id}")
                else:
                    logger.error(f'Ошибка при исключении из {chat_type}: {e}')
            except ChatNotFound:
                logger.error(f"{chat_type.capitalize()} {chat_id} не найден")
            except Exception as e:
                logger.error(f'Неожиданная ошибка при исключении из {chat_type}: {e}')

        # Попытка бана в канале
        await try_ban(const.channel_id, user_id, "канала")

        # Попытка бана в чате
        await try_ban(const.chat_id, user_id, "чата")
