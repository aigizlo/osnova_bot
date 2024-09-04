from get_conn import create_connection
from logger import logger
import mysql.connector
from datetime import datetime, timedelta


class QueryExecutionError(Exception):
    pass


def execute_query(query, params=None):
    try:
        with create_connection() as mydb:
            with mydb.cursor() as mycursor:
                if params:
                    mycursor.execute(query, params)
                else:
                    mycursor.execute(query)
                return mycursor.fetchall()
    except Exception as e:
        logger.error(f"PROCESS:execute_query, запрос {query}, {params}.  Ошибка - {e}")
        raise QueryExecutionError(f"Ошибка при выполнении запроса : {query},Error -  {e}")


sql_check_promo_code = """
SELECT period, used, create_date FROM promo_codes 
WHERE code = %s
"""

sql_update_promo_code = """
UPDATE promo_codes
SET used = TRUE
WHERE code = %s
"""

sql_check_existing_sub = """
SELECT subscription_id FROM subscriptions 
WHERE user_id = %s AND stop_date > NOW()
"""

sql_get_subscription_id = "SELECT LAST_INSERT_ID()"

sql_get_start_date = "SELECT start_date FROM subscriptions WHERE subscription_id = %s"

sql_get_sub_info = """
SELECT stop_date, is_active
FROM subscriptions
WHERE user_id = %s
ORDER BY stop_date DESC
LIMIT 1
"""


def check_promo_code(promo_code):
    # Получаем информацию о промокоде
    result = execute_query(sql_check_promo_code, (promo_code,))
    print(result, 'result')
    if not result:
        return False, "Промокод не найден"  # Промокод не найден
    period, used, create_date = result[0]
    # Проверяем срок действия (не более 3 дней)
    current_date = datetime.now()
    if (current_date - create_date).days > 3:
        return False, "Срок действия истек"  # Срок действия истек
    if used == 1:
        return False, "Промокод уже использован"  # Промокод уже использован
    return True, period


sql_insert_subscription = """
INSERT INTO subscriptions (user_id, duration_months, promo_code, start_date, stop_date)
VALUES (%s, %s, %s, NOW(), %s)
"""


def activate_subscription(user_id, period, promo_code=None):
    # Проверяем, есть ли у пользователя уже активная подписка
    existing_sub = execute_query(sql_check_existing_sub, (user_id,))
    if existing_sub:
        return "У пользователя уже есть активная подписка"

    start_date = datetime.now()
    stop_date = start_date + timedelta(days=period)

    try:
        execute_query(sql_insert_subscription, (user_id, period, promo_code, stop_date))

        if promo_code:
            print('промокод есть, делаем его использованным в базе')
            execute_query(sql_update_promo_code, (promo_code,))
        txt = '''🥳 Поздравляем!  

🎁 Вы получили по промокоду месячную подписку в клуб "ОСНОВА" '''
        return txt
    except QueryExecutionError as e:
        logger.error(f"Ошибка при активации подписки: {e}")
        return "Произошла ошибка при активации подписки"


def get_subscription_info(user_id):
    result = execute_query(sql_get_sub_info, (user_id,))
    if result:
        stop_date, is_active = result[0]
        current_date = datetime.now()
        if is_active == 1 and stop_date > current_date:
            return stop_date.strftime("%Y-%m-%d")
        else:
            return False
    else:
        return False


def format_date_string(date_string):
    # Словарь для перевода названий месяцев
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }

    # Пытаемся распарсить строку в объект datetime
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    # Форматируем дату в нужный формат
    day = date_object.day
    month = months[date_object.month]
    year = date_object.year
    return f"{day} {month} {year} года"


def my_tarif_info(date=None):
    if date:
        txt = f"""
📚 Продукт: "ОСНОВА"

🗓 Тарифный план:
— ваша подписка активна до {date}

🚨 Оплачивая или продливая подписку, Вы принимаете условия Пользовательского соглашения и Политики конфиденциальности."""
        return txt
    txt = """
📚 Продукт: "ОСНОВА"

🗓 Тарифный план:
— У вас отсутствует активная подписка!

— Сумма к оплате: 15 USD
— Период: 30 дней
— Тип платежа: Автоплатеж с интервалом в 30 дней

После оплаты будет предоставлен доступ:

— Канал «ОСНОВА»
— Чат «ФУНДАМЕНТАЛИСТЫ»

🚨 Оплачивая подписку, Вы принимаете условия Пользовательского соглашения и Политики конфиденциальности."""

    return txt