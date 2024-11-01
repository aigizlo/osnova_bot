# -*- coding: utf-8 -*-
import time

from aiogram import Bot  # Correct import for Bot
import const
import text
from config import err_send
from logger import logger
from user_data import execute_query
import keyboards

bot = Bot(token=const.token)

# запрос для получения ключей которые скоро истекут
sql_get_user_id_Xday_ago_registration = """SELECT u.user_id FROM users u LEFT JOIN (     SELECT user_id, MAX(subscription_id) as 
last_sub_id     FROM subscriptions     GROUP BY user_id ) last_sub ON u.user_id = last_sub.user_id LEFT JOIN 
subscriptions s ON last_sub.last_sub_id = s.subscription_id WHERE DATE(u.data) = DATE(NOW() - INTERVAL %s DAY)   AND (
s.is_active = 0 OR s.is_active IS NULL)
"""

days = [3, 6, 9]


async def send_notify():
    logger.info("Начинаем процесс уведомлений для пользователей не купивших подписку")
    try:
        for day in days:
            expired_sub_users = execute_query(sql_get_user_id_Xday_ago_registration, (day,))

            for user in expired_sub_users:
                telegram_id = user[0]
                if day == 3:
                    try:
                        await bot.send_message(chat_id=telegram_id,
                                               text=text.text_3_days_notify,
                                               parse_mode="HTML",
                                               reply_markup=keyboards.keyboard_period())
                        logger.info(f'text_3_days_notify , был отправлен {telegram_id}')
                    except Exception as e:
                        logger.error(f"Ошибка при отправке возможно в бан юзером - {e}")
                if day == 6:
                    try:
                        await bot.send_message(chat_id=telegram_id,
                                               text=text.text_6_days_notify,
                                               parse_mode="HTML",
                                               reply_markup=keyboards.keyboard_period())
                        logger.info(f'text_6_days_notify , был отправлен {telegram_id}')
                    except Exception as e:
                        logger.error(f"Ошибка при отправке возможно в бан юзером - {e}")
                if day == 9:
                    try:
                        await bot.send_message(chat_id=telegram_id,
                                               text=text.text_9_days_notify,
                                               parse_mode="HTML",
                                               reply_markup=keyboards.keyboard_period())
                        logger.error(f"Ошибка при отправке возможно в бан юзером - {e}")
                    except Exception as e:
                        logger.error(f"Ошибка при отправке  - {e}")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомлений для людей без подписки - {e}")
        await bot.send_message(chat_id=err_send,
                               text=f"Ошибка при отправке уведомлений для людей без подписки - {e}")

if __name__ == '__main__':
    import asyncio

    asyncio.run(send_notify())
