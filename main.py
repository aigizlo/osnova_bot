# -*- coding: utf-8 -*-
import asyncio
import logging
from aiogram import Dispatcher
from aiogram.utils import executor
from links import tracker
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import const

from handlers.admin_command import create_promo
from handlers.handlers import *
from handlers.handlers_main_menu import *
from aiogram import types

from handlers.handlers_promo import select_promo_code
from keyboards import set_default_commands
# from keyboards.admin_buutons import set_default_commands
from logger import logger
import user_data
import keyboards
from aiogram.utils.exceptions import ChatNotFound


select_promo_code
create_promo
scheduler = AsyncIOScheduler()

@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    referer_user_id = message.get_args()
    try:
        referer_user_id = int(referer_user_id)
        # Установка состояния
        await state.set_state(MyStates.select_period)
        try:
            new_user = user_data.if_new_user(user_id, first_name, referer_user_id, last_name, user_name)
            if new_user:
                # Отправка сообщений для нового пользователя
                await bot.send_message(chat_id=user_id,
                                       text=text.instruction,
                                       parse_mode="HTML", reply_markup=keyboards.main_menu())
                await asyncio.sleep(1)  # Небольшая задержка между сообщениями

                logging.info(f"INFO: NEW USER - tg: {user_id}, user_id: {new_user}, "
                             f"username: {user_name}, referer: {referer_user_id}")
                if referer_user_id:
                    try:
                        await bot.send_message(referer_user_id,
                                               f'По вашей ссылке зарегистрирован пользователь {first_name}, {last_name}, {user_name}')
                    except Exception as e:
                        logger.error('Ошибка', e)
            # Отправка основного сообщения (для новых и существующих пользователей)
            await bot.send_message(chat_id=user_id,
                                   text=text.product,
                                   reply_markup=keyboards.keyboard_period())
            await bot.send_message(chat_id=user_id,
                                   text="Главное меню",
                                   reply_markup=keyboards.main_menu())

        except Exception as e:
            error_message = f"Ошибка при обработке команды start: {e}"
            await bot.send_message(config.err_send, error_message)

            logging.error(error_message)
    except Exception as e:
        logger.info(f"Ссылка для трафика")
        hash_link = referer_user_id
        tracker.track_link(hash_link)
        logger.info(f'перешли по ссылке {hash_link}')
        await bot.send_message(chat_id=user_id,
                               text=text.product,
                               reply_markup=keyboards.keyboard_period())
        await bot.send_message(chat_id=user_id,
                               text="Главное меню",
                               reply_markup=keyboards.main_menu())


# def job_function():
#     get_expired_keys_info()


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(config.err_send, "Бот Запущен")


if __name__ == '__main__':
    # scheduler.add_job(job_function, IntervalTrigger(seconds=3))
    # scheduler.start()

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    logger.info('Бот запущен')



"""SELECT
    u.user_id,
    u.username,
    COUNT(r.user_id) AS referral_count,
    COALESCE(SUM(b.amount), 0) AS balance,
    s.is_active AS subscription,
    MAX(s.start_date) AS start_date,
    MAX(s.stop_date) AS stop_date
FROM
    users u
LEFT JOIN
    users r ON u.user_id = r.referer_id
LEFT JOIN
    (SELECT user_id, SUM(amount) as amount
     FROM balance
     GROUP BY user_id) b ON u.user_id = b.user_id
LEFT JOIN
    subscriptions s ON u.user_id = s.user_id AND s.is_active = 1
GROUP BY
    u.user_id, u.username
ORDER BY
    referral_count DESC;"""

