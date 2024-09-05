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

sql_add_ref_balance = """
    INSERT INTO balance (user_id, amount, transaction_type, description)
    VALUES (%s, %s, 'referral', %s)
    """


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


def add_referral_balance(user_id, amount, description):
    values = (user_id, amount, description)
    execute_query(sql_add_ref_balance, values)


# def subcribe_info


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


# def searche_user_id_with_user_name(user_name):
#     try:
#         query = """SELECT user_id FROM users WHERE username = %s"""
#         result = execute_query(query, (user_name,))
#         if result:
#             return result[0][0]
#         else:
#             return None
#     except Exception as e:
#         logger.error(f"QUERY_ERROR - searche_with_usr_name - {e}")
#         return None


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
        print('мы тут')
        info = execute_query(sql_user_info_user_name, (user_name,))
        print(info,' info')
    if not info:
        return "Пользователь не найден"

    user_info = info[0]
    username = user_info[0]
    referer_id = user_info[1]
    referer_username = user_info[2]
    amount = user_info[3]
    if not amount:
        amount = 0
    stop_date = user_info[4]
    is_active = user_info[5]

    text = f"Информация о пользователе:\n"
    text += f"Имя: {username}\n"
    if referer_id:
        text += f"Реферер: @{referer_username} ({referer_id})\n"
    else:
        text += f"Реферер: Нет\n"
    text += f"Баланс: {amount}\n"
    text += f"Дата окончания подписки: {'Да' if stop_date else 'Нет'}\n"
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
