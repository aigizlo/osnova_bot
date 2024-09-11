# -*- coding: utf-8 -*-

from aiogram import Bot  # Correct import for Bot
import const
import text
from logger import logger
from user_data import execute_query
from keyboards import renewal_sub


bot = Bot(token=const.token)

# запрос для получения ключей которые скоро истекут
sql_get_expired_sub_2days = """
SELECT user_id, duration_months
FROM subscriptions
WHERE stop_date <= NOW() + INTERVAL 2 DAY AND is_active = 1;
"""



# корректируем дни, дней, день
def plural_days(days):
    if 10 < days % 100 < 20:
        return f"{days} дней"
    else:
        rem = days % 10
        if rem == 1:
            return f"{days} день"
        elif 2 <= rem <= 4:
            return f"{days} дня"
        else:
            return f"{days} дней"


async def send_notify():
    logger.info("Starting notification process")
    expired_sub_users = execute_query(sql_get_expired_sub_2days)
    for user in expired_sub_users:
        telegram_id = user[0]
        months = user[1]
        months = months // 30
        if months < 3:
            await bot.send_message(chat_id=telegram_id,
                                   text=text.text_expired_sub_1month,
                                   parse_mode="HTML",
                                   reply_markup=renewal_sub())
            return
        if months >= 3 < 12:
            await bot.send_message(chat_id=telegram_id,
                                   text=text.text_expired_sub_3month,
                                   parse_mode="HTML",
                                   reply_markup=renewal_sub())
            return
        if months >= 12:
            await bot.send_message(chat_id=telegram_id,
                                   text=text.text_expired_sub_12month,
                                   parse_mode="HTML",
                                   reply_markup=renewal_sub())
            return




if __name__ == '__main__':
    import asyncio
    while True:
        asyncio.run(send_notify())
        await asyncio.sleep(60)
