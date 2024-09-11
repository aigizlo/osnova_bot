from get_conn import create_connection
from logger import logger
import mysql.connector
import get_conn
from datetime import datetime, timedelta

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

sql_insert_subscription = """
INSERT INTO subscriptions (user_id, duration_months, start_date, stop_date)
VALUES (%s, %s, NOW(), %s)
"""

sql_renewal_subscription = """
UPDATE subscriptions
SET stop_date = DATE_ADD(stop_date, INTERVAL %s DAY)
WHERE user_id = %s
"""

sql_get_sale_stats = '''
SELECT 
    COALESCE(SUM(tariff_1_month), 0) AS sales_1_month,
    COALESCE(SUM(tariff_3_months), 0) AS sales_3_months,
    COALESCE(SUM(tariff_12_months), 0) AS sales_12_months,
    COALESCE(SUM(total_sales), 0) AS total_sales
FROM sales_stat;

'''


def activate_or_renewal_subscription(user_id, period):
    print(period, ' period')
    # Проверяем, есть ли у пользователя уже активная подписка
    existing_sub = get_conn.execute_query(sql_check_existing_sub, (user_id,))
    if existing_sub:
        get_conn.execute_query(sql_renewal_subscription, (period, user_id))
        return True, "Ваша подписка успешно продлена!"
        # return "У пользователя уже есть активная подписка"
    start_date = datetime.now()
    stop_date = start_date + timedelta(days=period)

    try:
        get_conn.execute_query(sql_insert_subscription, (user_id, period, stop_date))
        return True, None
    except get_conn.QueryExecutionError as e:
        logger.error(f"user_id - {user_id} - Ошибка при активации подписки: {e}")
        return False
    except Exception as e:
        logger.error(f"user_id - {user_id} - Ошибка при активации подписки: {e}")
        return False


def get_subscription_info(user_id):
    result = get_conn.execute_query(sql_get_sub_info, (user_id,))
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


tariff_columns = {
    '1month': 'tariff_1_month',
    '3months': 'tariff_3_months',
    '12months': 'tariff_12_months'
}


def increment_tariff_sale(tariff):
    query = f"""
    INSERT INTO sales_stat (date, {tariff_columns[tariff]})
    VALUES (CURDATE(), 1)
    ON DUPLICATE KEY UPDATE 
    {tariff_columns[tariff]} = {tariff_columns[tariff]} + 1,
    updated_at = CURRENT_TIMESTAMP
    """
    get_conn.execute_query(query)


def get_sale_stats():
    result = get_conn.execute_query(sql_get_sale_stats)
    return result


def sale_paracent(stats):

    m_all = int(stats[0][3])
    if m_all == 0:
        return 0, 0, 0, 0

    m_1 = int(stats[0][0]) / m_all * 100

    m_3 = int(stats[0][1]) / m_all * 100
    m_12 = int(stats[0][2]) / m_all * 100

    return m_1, m_3, m_12, m_all
