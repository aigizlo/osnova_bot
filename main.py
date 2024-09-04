import asyncio
import logging
from aiogram import Dispatcher
from aiogram.utils import executor

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.handlers import *
import text
from handlers.handlers_main_menu import *
from aiogram import types

from handlers.handlers_promo import select_promo_code
from logger import logger
import user_data
import keyboards.keyboards

select_promo_code

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
        await bot.send_message(config.err_send, error_message)

        logging.error(error_message)


# def job_function():
#     get_expired_keys_info()


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    # await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(config.err_send, "Бот Запущен")


if __name__ == '__main__':
    # scheduler.add_job(job_function, IntervalTrigger(seconds=3))
    # scheduler.start()

    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    logger.info('Бот запущен')
