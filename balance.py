from get_conn import create_connection
from logger import logger
import math
import sub
import user_data

# sub.used_promo_code(user_id=12321312,promo_code='NEWPROMO2024')
from user_data import execute_query


# создаем заявку
def add_withdrawal_request(user_id: int, amount: float, wallet: str):
    user_data.execute_query('''
    INSERT INTO withdrawal_requests (user_id, amount, status, wallet)
    VALUES (%s, %s, %s, %s)
    ''', (user_id, amount, 'pending', wallet))


# создаем заявку на покупку в базе
def create_pay_id(user_id, amount, promo_id=None):
    # Первый запрос: вставка данных
    insert_sql = '''INSERT INTO transactions (user_id, amount_paid, promo_id)
    VALUES (%s, %s, %s)
    '''

    execute_query(insert_sql, (user_id, amount, promo_id))

    # Второй запрос: получение последнего вставленного ID
    select_sql = 'SELECT MAX(transaction_id) AS last_transaction_id FROM transactions;'

    result = execute_query(select_sql)

    if result:
        return result[0][0]
    else:
        return None

def insert_invice_id(pay_id, invoice_id):
    update_pay_id = '''UPDATE transactions SET invoice_id = %s
    WHERE transaction_id = %s
    '''
    execute_query(update_pay_id, (str(invoice_id), pay_id))


def get_last_pay_id(user_id):
    select_sql = """
    SELECT t.transaction_id AS last_transaction_id, t.amount_paid
        FROM transactions t
    WHERE t.user_id = %s
        AND t.transaction_id = (
    SELECT MAX(transaction_id) 
        FROM transactions 
    WHERE user_id = %s);"""
    result = execute_query(select_sql, (user_id, user_id,))
    logger.info(result)
    logger.info('--------------')
    if result:
        return result[0][0]
    else:
        return None


def check_status_transactions(pay_id):
    sql = """SELECT status FROM transactions WHERE transaction_id = %s"""
    result = execute_query(sql, (pay_id,))
    if result:
        if result[0][0] == 1:
            return True
    return False


def update_status_payment(order_id):
    logger.info(f"Processing order_id: {order_id}")
    sql_get_status = """
    SELECT status FROM transactions WHERE transaction_id = %s"""

    result = execute_query(sql_get_status, (str(order_id),))  # Note the comma to make it a tuple

    logger.info(f"SELECT status result: {result}")

    if result:
        logger.info('Result found')
        if result[0][0] == 1:
            logger.info(f"Status is 1 for order_id: {order_id}")
            return True

    sql_update_status = """
    UPDATE transactions SET status = 1 WHERE transaction_id = %s
    """
    execute_query(sql_update_status, (str(order_id),))

    sql_get_amount_paid = """
    SELECT amount_paid FROM transactions WHERE transaction_id = %s"""
    result = execute_query(sql_get_amount_paid, (str(order_id),))

    amount = result[0][0]

    tariff = tariffs.get(amount)

    sub.increment_tariff_sale(tariff)

    logger.info(f"UPDATE result: sucssess")

    return False


def update_status_crypto_payment(invoice_id):
    logger.info(f"Processing invoice_id: {invoice_id}")
    sql_get_status = """
    SELECT status FROM transactions WHERE invoice_id = %s"""

    result = execute_query(sql_get_status, (str(invoice_id),))  # Note the comma to make it a tuple

    logger.info(f"SELECT status result: {result}")

    if result:
        logger.info('Result found')
        if result[0][0] == 1:
            logger.info(f"Status is 1 for order_id: {invoice_id}")
            return True

    sql_update_status = """
    UPDATE transactions SET status = 1 WHERE invoice_id = %s
    """
    execute_query(sql_update_status, (str(invoice_id),))

    sql_get_amount_paid = """
    SELECT amount_paid FROM transactions WHERE transaction_id = %s"""
    result = execute_query(sql_get_amount_paid, (str(invoice_id),))

    amount = result[0][0]

    tariff = tariffs.get(amount)

    sub.increment_tariff_sale(tariff)

    logger.info(f"UPDATE result: sucssess")

    return False

tariffs = {
    15.00: '1month',
    40.00: '3months',
    150.00: '12months',
}

# The following line should be removed or placed outside the function:
# raise QueryExecutionError(f"Ошибка при выполнении запроса : {query},Error -  {e}")


# # запрос для оплаты с реф баланса
# sql_pay_from_bonus_query = """INSERT INTO user_balance_ops
#             (user_id, optype, amount)
#                         VALUES (%s, 'bonus', -%s)"""
#
# #
# # запрос для начисления реферального бонуса
# sql_add_referral_bonus = """INSERT INTO user_balance_ops
#             (user_id, optype, amount)
#                         VALUES (%s, 'bonus', %s)"""
#
# def add_referral_bonus(user_id, purchase_amount):
#     try:
#         # Преобразуем purchase_amount в число с плавающей точкой, если это возможно.
#         # Если purchase_amount является строкой, которая содержит число, это будет работать.
#         # Если строка не может быть преобразована в число, будет сгенерировано исключение ValueError.
#         purchase_amount = float(purchase_amount)
#
#         # ищем юзер_айди реферера
#         referer_user_id = user_data.get_referrer_user_id(user_id)
#
#         if referer_user_id in partners:
#             bonus_rub = purchase_amount * partner_bonus
#             bonus_rub = math.floor(bonus_rub)
#         else:
#             bonus_rub = purchase_amount * coefficeint_bonus
#             bonus_rub = math.floor(bonus_rub)
#
#         execute_query(sql_add_referral_bonus, (referer_user_id, bonus_rub))
#         logger.info(f"REFERRAL_BONUS_SUCCESS: Начислен реферальный бонус user - "
#                     f"{referer_user_id}, на сумму {bonus_rub}")
#         return bonus_rub
#     except ValueError:
#         logger.error(f"REFERRAL_BONUS_FAILED: Ошибка, purchase_amount не является числом")
#         return False
#     except Exception as e:
#         logger.error(f"REFERRAL_BONUS_FAILED: Ошибка при начислении реферального бонуса - {e}")
#         return False
#
#
# def pay_from_referral_balance(user_id, amount):
#     current_balance = user_data.get_user_balance_bonus(user_id)
#     try:
#         execute_query(sql_pay_from_bonus_query, (user_id, amount))
#         logger.info(f"PROCESS:pay_from_referral_balance : Покупка на сумму {amount} прошла успешно, "
#                     f"пользователь - {user_id}")
#         return True
#
#     except Exception as e:
#         logger.ERROR(f"ERROR:pay_from_referral_balance : Произошла ошибка при покупке на сумму - {amount}, "
#                      f"у пользователя {user_id}, его баланс {current_balance}, "
#                      f"Ошибка: {e}")
#         return False
#
#
# #
# def money_back(user_id, money):
#     sql_add_referral_bonus = """INSERT INTO user_balance_ops
#                 (user_id, optype, amount)
#                             VALUES (%s, 'bonus', %s)"""
#     try:
#         execute_query(sql_add_referral_bonus, (user_id, money,))
#         logger.info(
#             f"MONEY BACK - SUCSSESS - возвращены средства на баланс user_id - {user_id}, cумма {money}")
#         return True
#     except Exception as e:
#         logger.error(
#             f"MONEY BACK - ERROR - средства НЕВОЗВРАЩЕНЫ на баланс user_id - {user_id}, cумма {money}, ошибка - {e}")
#         return False
#
#
# # cоздаем неоплаченный платеж в базе bills для покупки (НЕ ПРОДЛЕНИЕ)
# def creating_payment(amount, user_id):
#     try:
#
#         with create_connection() as mydb, mydb.cursor(buffered=True) as mycursor:
#
#             sql_create_bill = "INSERT INTO bills (amount, user_id) VALUES (%s, %s)"
#
#             mycursor.execute(sql_create_bill, (amount, user_id,))
#             pay_id = mycursor.lastrowid
#
#             logger.info(f"CREATE PAYMENT - SUCSSESS: user_id - {user_id}, amount - {amount}, pay_id - {pay_id}")
#
#         return mycursor.lastrowid
#
#     except Exception as e:
#         logger.error(f"CREATE PAYMENT - FAILED: user_id - {user_id}, amount - {amount}, ERROR - {e}")
#
#
# def creating_payment_for_renewal(amount, user_id, key_id):
#     try:
#
#         with create_connection() as mydb, mydb.cursor(buffered=True) as mycursor:
#
#             sql_create_bill = "INSERT INTO bills (amount, user_id, key_id) VALUES (%s, %s, %s)"
#
#             mycursor.execute(sql_create_bill, (amount, user_id, key_id,))
#
#             pay_id = mycursor.lastrowid
#
#             logger.info(f"CREATE PAYMENT - SUCSSESS: user_id - {user_id}, amount - {amount}, pay_id - {pay_id}")
#
#         return mycursor.lastrowid
#
#     except Exception as e:
#         logger.error(f"CREATE PAYMENT - FAILED: user_id - {user_id}, amount - {amount}, ERROR - {e}")
