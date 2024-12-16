# -*- coding: utf-8 -*-
import time
import handlers.handlers_main_menu
from aiogram import Bot
import const
import text
import user_data
from config import err_send
from logger import logger
from user_data import execute_query
from keyboards import renewal_sub, keyboard_period2

bot = Bot(token=const.token)

sql_get_expired_sub_Xdays = """
SELECT user_id
FROM subscriptions
WHERE DATE(stop_date) = DATE(NOW() + INTERVAL %s DAY)
AND is_active = 1;
"""


async def send_notify_exrpd():
    logger.info("Начинается процесс отправки уведомлений и об истекающих подписках")
    try:

        for day in [7, 2, 1]:
            expired_sub_users = execute_query(sql_get_expired_sub_Xdays, (day,))
            if not expired_sub_users:
                print('пусто')
                continue
            print(expired_sub_users)
            for user in expired_sub_users:
                telegram_id = user[0]
                if day == 7:
                    txt = text.text_expired_sub_7day
                if day == 2:
                    txt = text.text_expired_sub_1month
                if day == 1:
                    txt = text.text_expired_sub_1day
                try:
                    await bot.send_message(chat_id=telegram_id,
                                           text=txt,
                                           parse_mode="HTML",
                                           reply_markup=keyboard_period2())
                except Exception as e:
                    logger.error(f"Ошибка при отправке возможно в бан юзером - {e}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомлений и об истекающих подписках- {e}")
        await bot.send_message(chat_id=err_send,
                               text=f"Ошибка при отправке уведомлений и об истекающих подписках - {e}")


sql_get_user_id_Xday_ago_registration = """SELECT u.user_id FROM users u LEFT JOIN (     SELECT user_id, MAX(subscription_id) as 
last_sub_id     FROM subscriptions     GROUP BY user_id ) last_sub ON u.user_id = last_sub.user_id LEFT JOIN 
subscriptions s ON last_sub.last_sub_id = s.subscription_id WHERE DATE(u.data) = DATE(NOW() - INTERVAL %s DAY)   AND (
s.is_active = 0 OR s.is_active IS NULL)
"""


async def send_notify():
    days = [1, 2]
    logger.info("Начинаем процесс уведомлений для пользователей не купивших подписку")
    try:
        for day in days:
            expired_sub_users = execute_query(sql_get_user_id_Xday_ago_registration, (day,))

            for user in expired_sub_users:
                telegram_id = user[0]
                if day == 1:
                    try:
                        await bot.send_message(chat_id=telegram_id,
                                               text=text.text_1_day_notify,
                                               parse_mode="HTML")
                        logger.info(f'text_1_day_notify , был отправлен {telegram_id}')
                    except Exception as e:
                        logger.error(f"Ошибка при отправке возможно в бан юзером - {e}")
                if day == 2:
                    try:
                        await bot.send_message(chat_id=telegram_id,
                                               text=text.text_2_days_notify,
                                               parse_mode="HTML")
                        logger.info(f'text_6_days_notify , был отправлен {telegram_id}')
                    except Exception as e:
                        logger.error(f"Ошибка при отправке возможно в бан юзером - {e}")

    except Exception as e:
        logger.error(f"Ошибка при отправке уведомлений для людей без подписки - {e}")
        await bot.send_message(chat_id=err_send,
                               text=f"Ошибка при отправке уведомлений для людей без подписки - {e}")


# выгояем из группы тех, у кого нет подписки
async def check_subscrypt():
    user_ids = user_data.get_all_users()
    user_ids = [user_id[0] for user_id in user_ids]
    try:
        for user in user_ids:
            await handlers.handlers_main_menu.delete_from_channel(user)
    except Exception as e:
        logger.error(f"Ошибка при удалении юзеров из канала - {e}")


if __name__ == '__main__':
    import asyncio

    asyncio.run(send_notify_exrpd())
    time.sleep(5)
    asyncio.run(send_notify())
    time.sleep(5)
    asyncio.run(check_subscrypt())
