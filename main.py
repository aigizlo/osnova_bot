import asyncio
import logging
from aiogram import Dispatcher
from aiogram.utils import executor

from handlers.send_all import show_rassilka
from links import tracker
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers.admin_command import create_promo
from handlers.handlers import *
from handlers.handlers_main_menu import *
from aiogram import types

from handlers.handlers_promo import select_promo_code
from keyboards import set_default_commands
from logger import logger
import user_data
import keyboards

show_rassilka
select_promo_code
create_promo
scheduler = AsyncIOScheduler


@dp.message_handler(commands=['start'], state="*")
async def process_start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    referer_user_id = message.get_args()
    logger.info(f'{referer_user_id}, referer_user_id')
    try:
        if not referer_user_id.isdigit():
            hash_link = referer_user_id
            tracker.track_link(hash_link)
            logger.info(f'перешли по отслеживаемой ссылке {hash_link}')
            referer_user_id = None

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

                logging.info(f"INFO: NEW USER - tg: {user_id}, \n"
                             f"user_id: {new_user}, \n"
                             f"username: {user_name}, \n"
                             f"referer: {referer_user_id}")

                if referer_user_id:
                    try:
                        txt = text.ref_send_if_reg(first_name, last_name, user_name)
                        logger.info(txt)
                        logger.info('----------------------')
                        await bot.send_message(referer_user_id, txt, parse_mode="HTML")
                    except Exception as e:
                        logger.error('Ошибка', e)

                    await bot.send_message(chat_id=user_id,
                                           text="Главное меню",
                                           parse_mode="HTML",
                                           reply_markup=keyboards.main_menu())
                    # Уведомляем админа о новеньком
                    for admin in const.admins_notify:
                        await bot.send_message(chat_id=admin,
                                               text=f"ℹ️ NEW USER"
                                                    f"📱 {new_user}\n"
                                                    f"👥 UserName: {user_name}, \n"
                                                    f"👤 First_Name: {first_name}\n"
                                                    f"👤 Last_Name: {first_name}\n"
                                                    f"📲 Ref: {referer_user_id}")
            # Отправка основного сообщения (для новых и существующих пользователей)
            await bot.send_message(chat_id=user_id,
                                   text=text.product,
                                   reply_markup=keyboards.keyboard_period())

        except Exception as e:
            error_message = f"Ошибка при обработке команды start: {e}"
            await bot.send_message(config.err_send, error_message)

            logging.error(error_message)
    except Exception as e:
        logger.error(f"Ошибка {e}")


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


async def on_startup_notify(dp: Dispatcher):
    await dp.bot.send_message(config.err_send, "Бот Запущен")


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    logger.info('Бот запущен')
