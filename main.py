import asyncio
import logging
from aiogram.dispatcher import FSMContext


from aiogram.dispatcher.filters import state

from config import admin, err_send
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Dispatcher

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.utils import executor

from handlers.handlers_promo import select_promo_code, process_key_name
from handlers.handlers import *
from handlers.send_all import *
# from handlers.admin_command import user_info_command, prolong_key
import text
from handlers.handlers_main_menu import *
from aiogram import types
from logger import logger
import user_data
import keyboards.keyboards

# user_info_command
# show_rassilka
# get_posttext
# get_photo
# get_photo_id
# get_video
# get_video_id
# get_testpost
# sendposts
# cancel_post
# select_promo_code
# prolong_key
# process_key_name
# admin_commands


scheduler = AsyncIOScheduler()


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    referer_user_id = message.get_args()

    logger.info(f"Start command received from {telegram_id}, {user_name}, {first_name}")

    # Установка состояния
    await state.set_state(MyStates.select_period)
    logger.info(f"State was set to {MyStates.select_period}")

    try:
        new_user = user_data.if_new_user(telegram_id, first_name, referer_user_id, last_name, user_name)
        logger.info(f"New user status: {new_user}")

        if new_user:
            # Отправка сообщений для нового пользователя
            await bot.send_message(chat_id=telegram_id,
                                   text=text.instruction,
                                   parse_mode="HTML", reply_markup=keyboards.keyboards.main_menu())
            await asyncio.sleep(1)  # Небольшая задержка между сообщениями

        # Отправка основного сообщения (для новых и существующих пользователей)
        await bot.send_message(chat_id=telegram_id,
                               text=text.product,
                               reply_markup=keyboards.keyboards.keyboard_period())
        await bot.send_message(chat_id=telegram_id,
                               text="Главное меню",
                               reply_markup=keyboards.keyboards.main_menu())

        if new_user:
            logging.info(f"INFO: NEW USER - tg: {telegram_id}, user_id: {new_user}, "
                         f"username: {user_name}, referer: {referer_user_id}")

    except Exception as e:
        error_message = f"Ошибка при обработке команды start: {e}"
        await bot.send_message(err_send, error_message)
        logging.error(error_message)

# @dp.message_handler(commands=['start'], state="*")
# async def process_start_command(message: types.Message, state: FSMContext):
#     telegram_id = message.from_user.id
#     user_name = message.from_user.username
#     first_name = message.from_user.first_name
#     last_name = message.from_user.last_name
#     referer_user_id = message.get_args()
#     print(message)
#     await state.set_state(MyStates.select_period)
#     logger.info(f"State was set to {MyStates.select_period}")
#
#     logger.info(f"start command {telegram_id}, {user_name}, {first_name}")
#     try:
#         if message.message_id:
#             await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
#     except aiogram.utils.exceptions.MessageCantBeDeleted:
#         logger.info("Сообщение не может быть удалено.")
#     try:
#         new_user = user_data.if_new_user(telegram_id, first_name, referer_user_id, last_name, user_name)
#         print(new_user)
#         if not new_user:
#             await bot.send_message(chat_id=telegram_id,
#                                    text=text.product,
#                                    parse_mode="HTML",
#                                    reply_markup=keyboards.keyboards.keyboard_period())
#             return
#
#         await bot.send_message(chat_id=telegram_id,
#                                text=text.instruction,
#                                parse_mode="HTML")
#         await asyncio.sleep(1)
#         await bot.send_message(chat_id=telegram_id,
#                                text=text.product,
#                                parse_mode="HTML",
#                                reply_markup=keyboards.keyboards.keyboard_period())
#
#         logging.info(f"INFO: NEW USER - tg :, user_id - {new_user}, tg - {telegram_id}, "
#                      f"username : {user_name}, "
#                      f"{referer_user_id}")
#
#     except Exception as e:
#         await bot.send_message(err_send, f"Ошибка при регистрации нового пользователя ошибка - {e}")
#         logging.error(f"ERROR:NEW USER - Ошибка при добавлении нового пользователя "
#                       f"tg - {telegram_id}, "
#                       f"ошибка - {e}")


# def job_function():
#     get_expired_keys_info()


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    # await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(err_send, "Бот Запущен")


if __name__ == '__main__':
    # scheduler.add_job(job_function, IntervalTrigger(seconds=3))
    # scheduler.start()

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    logger.info('Бот запущен')
