# -*- coding: utf-8 -*-
from get_conn import create_connection
from logger import logger
import mysql.connector
import get_conn
from datetime import datetime, timedelta
import random
import string

sql_check_promo_code = """
SELECT period, used, create_date FROM promo_codes 
WHERE code = %s
"""

sql_procrochka = '''
DELETE FROM promo_codes WHERE create_date < DATE_SUB(CURDATE(), INTERVAL 3 DAY)'''

sql_delete_used_promo = '''
DELETE FROM promo_codes WHERE used = 1'''

sql_update_promo_code = """
UPDATE promo_codes
SET used = TRUE,
user_id = %s
WHERE code = %s
"""

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
        result = get_conn.execute_query(sql_check_promo_code, (promo_code,))
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
        logger.error(f'ERROR - check_promo_code - {promo_code} - {e}')
        return False, "Произошла ошибка, обратитесь к администратору"


def status_used_promo_code(user_id, promo_code):
    get_conn.execute_query(sql_update_promo_code, (user_id, promo_code,))


def clear_used_promo():
    get_conn.execute_query(sql_delete_used_promo)
    get_conn.execute_query(sql_procrochka)


def create_promo_code(code, period):
    result = get_conn.execute_query(sql_check_promo_codes, (code,))
    if result:
        return False, "Такой промокод уже есть"
    get_conn.execute_query(sql_new_promo_code, (code, period))
    sql_lst_promo_id = 'SELECT MAX(promo_id) FROM promo_codes;'
    promo_id = get_conn.execute_query(sql_lst_promo_id)
    logger.info(promo_id)
    logger.info('-------------============')
    return promo_id[0][0], "Промокод успешно создан"


def generate_promo_code(period):
    letters = string.ascii_letters
    result = False
    while not result:
        promo_code = ''.join(random.choice(letters) for _ in range(5))
        promo_id = create_promo_code(promo_code, period)
        if promo_id:
            break
    return promo_code, promo_id


def get_promo_id_from_transactions(pay_id):
    sql = """
    SELECT pc.promo_id, pc.code, period
    FROM transactions t
    JOIN promo_codes pc ON t.promo_id = pc.promo_id
    WHERE t.transaction_id= %s"""
    promo_id = get_conn.execute_query(sql, (pay_id,))
    if promo_id:
        return promo_id[0]
    else:
        False


def generate_promo_code_report():
    # Retrieve all promo codes from the table
    sql_get_promo_info = "SELECT code, period, used, user_id FROM promo_codes"
    promo_codes = get_conn.execute_query(sql_get_promo_info)
    # Generate the report
    report = "📊 Promo Code Report 📊\n"
    for promo_code in promo_codes:
        used = promo_code[2]
        if used == 1:
            used = "Да"
        else:
            used = "НЕТ"
        report += f"ПРОМОКОД: {promo_code[0]}\nПЕРИОД: {promo_code[1]} Дней\nИСПОЛЬЗОВАН: {used}\nUser ID: {promo_code[3]}\n\n"

    return report
