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
SET used = TRUE,
user_id = %s
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

sql_check_promo_codes = "SELECT * FROM promo_codes WHERE code = %s"

sql_new_promo_code = """
INSERT INTO promo_codes (code, period)
VALUES (%s, %s)
"""


def check_promo_code(promo_code):
    # Получаем информацию о промокоде
    try:
        result = execute_query(sql_check_promo_code, (promo_code,))
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
    except Exception as e:
        logger.error(f'ERROR - check_promo_code - {promo_code}')
        return False, "Произошла ошибка, обратитесь к администратору"


sql_insert_subscription = """
INSERT INTO subscriptions (user_id, duration_months, start_date, stop_date)
VALUES (%s, %s, NOW(), %s)
"""

sql_renewal_subscription = """
UPDATE subscriptions
SET stop_date = DATE_ADD(stop_date, INTERVAL %s DAY)
WHERE user_id = %s
"""


# def renewal_subscription(user_id, days):
#     execute_query(sql_renewal_subscription, (days, user_id))


def activate_or_renewal_subscription(user_id, period):
    # Проверяем, есть ли у пользователя уже активная подписка
    existing_sub = execute_query(sql_check_existing_sub, (user_id,))
    if existing_sub:
        execute_query(sql_renewal_subscription, (period, user_id))
        return True, "Ваша подписка успешно продлена!"
        # return "У пользователя уже есть активная подписка"
    start_date = datetime.now()
    stop_date = start_date + timedelta(days=period)
    try:
        execute_query(sql_insert_subscription, (user_id, period, stop_date))
        return True, None
    except QueryExecutionError as e:
        logger.error(f"user_id - {user_id} - Ошибка при активации подписки: {e}")
        return False
    except Exception as e:
        logger.error(f"user_id - {user_id} - Ошибка при активации подписки: {e}")
        return False


def status_used_promo_code(user_id, promo_code):
    execute_query(sql_update_promo_code, (user_id, promo_code,))


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


def create_promo_code(code, period):
    result = execute_query(sql_check_promo_codes, (code,))
    if result:
        return False, "Такой промокод уже есть"
    execute_query(sql_new_promo_code, (code, period))
    return True, "Промокод успешно создан"


def generate_promo_code_report():
    # Retrieve all promo codes from the table
    sql_get_promo_info = "SELECT code, period, used, user_id FROM promo_codes"
    promo_codes = execute_query(sql_get_promo_info)
    # Generate the report
    report = "📊 Promo Code Report 📊\n"
    report += "-------------------------\n"
    for promo_code in promo_codes:
        used = promo_code[2]
        if used == 1:
            used = "Да"
        else:
            used = "НЕТ"
        report += f"ПРОМОКОД: {promo_code[0]}\nПЕРИОД: {promo_code[1]} Дней\nИСПОЛЬЗОВАН: {used}\nUser ID: {promo_code[3]}\n\n"

    return report
