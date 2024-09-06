import mysql.connector
from const import host, user, password, database
from logger import logger


def create_connection():
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=True
        )

        # logger.info('DB_CONNECT_SUCCESS')
        return conn  # Возвращаем объект соединения
    except mysql.connector.errors.InterfaceError as err:
        logger.error(f'DB_CONNECT_ERROR: %s %s, ошибка - {err}')
        return None


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
