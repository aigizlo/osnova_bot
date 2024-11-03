# -*- coding: utf-8 -*-
import get_conn
from get_conn import create_connection
from logger import logger
import sub


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


sql_all_users_info = """
SELECT
    u.user_id,
    u.username,
    COUNT(r.user_id) AS referral_count,
    COALESCE(SUM(b.amount), 0) AS balance,
    s.is_active AS subscription,
    MAX(s.start_date) AS start_date,
    MAX(s.stop_date) AS stop_date,
    ru.username AS referer_username
FROM
    users u
LEFT JOIN
    users r ON u.user_id = r.referer_id
LEFT JOIN
    (SELECT user_id, SUM(amount) as amount
     FROM balance
     GROUP BY user_id) b ON u.user_id = b.user_id
LEFT JOIN
    subscriptions s ON u.user_id = s.user_id AND s.is_active = 1
LEFT JOIN
    users ru ON u.referer_id = ru.user_id
GROUP BY
    u.user_id, u.username, ru.username
ORDER BY
    referral_count DESC"""

sql_get_ref_balance = """
SELECT 
    SUM(CASE 
        WHEN transaction_type = 'referral' THEN amount
        WHEN transaction_type = 'credit' THEN amount
        WHEN transaction_type = 'debit' THEN -amount
        ELSE 0
    END) AS balance
FROM balance
WHERE user_id = %s
GROUP BY user_id;
"""

sql_get_count_referrals = '''
SELECT 
    COUNT(r.user_id) AS referral_count
FROM 
    users u
LEFT JOIN 
    users r ON u.user_id = r.referer_id
WHERE 
    u.user_id = %s
GROUP BY 
    u.user_id, u.first_name, u.username;'''

sql_get_users = "SELECT telegram_id FROM users"

slq_get_referrer_user_id = """SELECT referer_id FROM users WHERE user_id = %s"""


def get_list_admins_telegram_id():
    sql_query = "SELECT telegram_id FROM users WHERE admin = 1"
    result = execute_query(sql_query)
    # Преобразовываем кортежи в int значения
    telegram_ids = [entry[0] for entry in result]
    return telegram_ids


# используем для получения всех tg_id пользователей
def get_all_users():
    result = execute_query(sql_get_users)
    users = [value for _tuple in result for value in _tuple]
    return users


def count_referrals(user_id):
    try:
        result = execute_query(sql_get_count_referrals, (user_id,))
        if result:
            return result[0][0]
        else:
            return 0
    except Exception as e:
        logger.error(f"QUERY_ERROR - count_referrals - {e}")


sql_add_ref_balance = """
    INSERT INTO balance (user_id, amount, transaction_type, description)
    VALUES (%s, %s, 'referral', %s)
    """


def add_referral_balance(user_id, amount, description=None):
    try:
        values = (user_id, amount, description)
        execute_query(sql_add_ref_balance, values)
        if amount > 0:
            logger.info(f"Баланс {amount}, начислен юзеру {user_id}")
            return True, f"Баланс {amount}, начислен юзеру {user_id}"
        else:
            logger.info(f"Баланс {amount}, снят с юзера {user_id}")
            return True, f"Баланс {amount}, снят с юзера {user_id}"

    except Exception as e:
        logger.error(f"Ошибка операции с балансом, {e}")
        return False, f"Ошибка операции с балансом {e}"


def referral_transactions(user_id, amount):
    amount = float(amount)
    price = amount
    # Cначала узнаем есть ли реферер у юзера
    sql_get_referer_user_id = """
    SELECT referer_id FROM users WHERE user_id = %s;
    """
    result = execute_query(sql_get_referer_user_id, (user_id,))

    if not result[0][0]:
        sub.update_sale_statistic(price, price)
        return False

    referer_id = result[0][0]

    amount = amount / 3

    result = add_referral_balance(referer_id, float(amount), "Реферальные начисления")

    sub.update_sale_statistic(price, price - amount)

    return result


def get_user_balance_bonus(user_id):
    try:
        result = execute_query(sql_get_ref_balance, (user_id,))
        if not result:
            return 0
        return result[0][0]
    except Exception as e:
        logger.error(f"QUERY_ERROR - get_user_balance_bonus - {e}")


def get_referrer_user_id(user_id):
    try:
        result = execute_query(slq_get_referrer_user_id, (user_id,))
        return result[0][0]
    except Exception as e:
        logger.error(f"QUERY_ERROR - get_referrer_user_id - {e}")


def check_user_in_system(telegram_id):
    try:
        with create_connection() as mydb:
            with mydb.cursor() as mycursor:
                sql_check_new_user = "SELECT * FROM users WHERE telegram_id = %s"
                mycursor.execute(sql_check_new_user, (telegram_id,))
                result = mycursor.fetchone()
                if not result:
                    return result
                return True
    except Exception as e:
        logger.error(f"ERROR:check_user_in_system - Ошибка базы данных: {e}")


def all_users():
    result = execute_query("""SELECT COUNT(*) FROM users;""")
    if not result:
        return 0
    return result[0][0]


def get_user_name_frst_name_last_name(user_id):
    try:
        query = """SELECT first_name, lastname,username FROM users WHERE user_id = %s"""
        result = execute_query(query, (user_id,))
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        logger.error(f"QUERY_ERROR - searche_with_usr_name - {e}")
        return None


sql_user_info_user_id = '''SELECT 
  u.username, 
  u.referer_id, 
  r.username AS referer_username, 
  b.amount, 
  s.stop_date, 
  s.is_active
FROM 
  users u 
  LEFT JOIN users r ON u.referer_id = r.user_id 
  LEFT JOIN balance b ON u.user_id = b.user_id 
  LEFT JOIN subscriptions s ON u.user_id = s.user_id 
WHERE 
  u.user_id = %s
'''

sql_user_info_user_name = '''SELECT 
  u.username, 
  u.referer_id, 
  r.username AS referer_username, 
  b.amount, 
  s.stop_date, 
  s.is_active
FROM 
  users u 
  LEFT JOIN users r ON u.referer_id = r.user_id 
  LEFT JOIN balance b ON u.user_id = b.user_id 
  LEFT JOIN subscriptions s ON u.user_id = s.user_id 
WHERE 
  u.username = %s
'''


def get_user_info(user_id=None, user_name=None):
    if user_id:
        info = execute_query(sql_user_info_user_id, (user_id,))
    elif user_name:
        info = execute_query(sql_user_info_user_name, (user_name,))
    if not info:
        return "Пользователь не найден"

    user_info = info[0]
    username = user_info[0]
    referer_id = user_info[1]
    referer_username = user_info[2]
    amount = user_info[3]
    if not amount:
        amount = 0

    # stop_date = sub.format_date_string(stop_date)
    is_active = user_info[5]

    text = f"Информация о пользователе:\n"
    text += f"Имя: {username}\n"
    if referer_id:
        text += f"Реферер: @{referer_username} ({referer_id})\n"
    else:
        text += f"Реферер: Нет\n"
    text += f"Баланс: {amount}\n"
    if user_info[4]:
        stop_date = user_info[4].strftime("%Y-%m-%d")
    else:
        stop_date = "НЕТ"
    text += f"Дата окончания подписки: {stop_date}\n"
    text += f"Активность подписки: {'Да' if is_active else 'Нет'}"

    return text


def if_new_user(user_id, first_name, referer_user_id, last_name, username):
    try:
        # Создаем соединение с базой данных
        with create_connection() as mydb:
            with mydb.cursor() as mycursor:
                # Проверяем наличие пользователя по user_id
                sql_check_new_user = "SELECT * FROM users WHERE user_id = %s"
                mycursor.execute(sql_check_new_user, (user_id,))

                result = mycursor.fetchone()

                # Если пользователь уже существует, возвращаем False
                if result:
                    return False
                # Если указан referer_id, проверяем его наличие в базе данных
                if referer_user_id:
                    sql_check_referer = "SELECT * FROM users WHERE user_id = %s"
                    mycursor.execute(sql_check_referer, (referer_user_id,))
                    referer_result = mycursor.fetchone()
                    logger.info(f"NEW USER : {user_id}, {username}, referer - None")

                    # Если referer_id не найден, даем None
                    if not referer_result:
                        logger.info(f"PROCESS : if_new_user - несуществующий referer {user_id}, {username}")
                        referer_user_id = None
                    # Добавляем нового пользователя с указанным refer_id
                    sql_insert_user = "INSERT INTO users (username, user_id, referer_id, lastname, first_name) VALUES " \
                                      "(%s, %s, %s, %s, %s) "
                    mycursor.execute(sql_insert_user, (username, user_id, referer_user_id, last_name, first_name))
                    logger.info(f"NEW USER : добавлен в базу {user_id}, {username}, referer - {referer_user_id}")
                else:
                    # Добавляем нового пользователя без refer_id
                    sql_insert_user = "INSERT INTO users (username, user_id, lastname, first_name) VALUES (%s, %s, " \
                                      "%s, %s) "
                    mycursor.execute(sql_insert_user, (username, user_id, last_name, first_name))
                    logger.info(f"NEW USER : добавлен в базу {user_id}, {username} - referer - None")
                return user_id
    except Exception as e:
        logger.error(f"ERROR:if_new_user - Ошибка базы данных: {e}")
        return None


def show_user_data():
    result = get_conn.execute_query(sql_all_users_info)
    return result


def show_links_info():
    sql = """select link, link_name, clicks from links"""
    result = get_conn.execute_query(sql)
    return result


sql_get_user_id_have_sub = '''
SELECT user_id FROM subscriptions WHERE is_active = 1;
'''

sql_get_user_id_have_not_sub = '''
SELECT u.user_id
FROM users u
LEFT JOIN subscriptions s ON u.user_id = s.user_id AND s.is_active = 1
WHERE s.user_id IS NULL OR s.is_active IS NULL
GROUP BY u.user_id
'''
sql_get_users_ = '''
SELECT user_id FROM users
'''


def get_user_id_have_not_sub():
    return execute_query(sql_get_user_id_have_not_sub)


def get_user_id_have_sub():
    return execute_query(sql_get_user_id_have_sub)


def get_all_users():
    return execute_query(sql_get_users_)


def get_status_withdraw(user_id):
    sql = """
    SELECT * FROM withdrawal_requests WHERE user_id = %s AND status = "pending";
    """
    result = execute_query(sql, (user_id,))

    if result:
        return result
    else:
        return False


def delete_withdraw_request(user_id):
    sql = """
    DELETE FROM withdrawal_requests WHERE user_id = %s AND status = "pending";
    """
    execute_query(sql, (user_id,))


def update_rules(digit, user_id):
    sql = """UPDATE users SET rules = %s
    WHERE user_id = %s"""
    execute_query(sql, (digit, user_id,))


def get_rules(user_id):
    sql = """SELECT rules FROM users
    WHERE user_id = %s"""
    result = execute_query(sql, (user_id,))

    return result[0]

