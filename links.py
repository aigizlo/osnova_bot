import mysql.connector
import uuid
import hashlib
from logger import logger
from get_conn import create_connection


class TrafficTracker:
    def __init__(self):
        self.connection = create_connection()
        self.cursor = self.connection.cursor()

    def __enter__(self):
        self.connection = create_connection()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, args=None):
        try:
            if not self.connection.is_connected():
                self.connection.reconnect()
            self.cursor.execute(query, args)
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            logger.error(f"QUERY_ERROR - {e}")

    def generate_link(self, bot_name, name):
        uid = uuid.uuid4()
        link_hash = hashlib.sha256(str(uid).encode()).hexdigest()[:8]
        link = f"t.me/{bot_name}?start={link_hash}"
        # Вставляем запись в таблицу links
        self.execute_query("INSERT INTO links (link, link_name, link_hash) VALUES (%s, %s, %s)",
                           (link, name, link_hash))
        return link

    def track_link(self, link_hash):
        # Инкрементируем счетчик для заданной ссылки
        self.execute_query("UPDATE links SET clicks = clicks + 1 WHERE link_hash = %s", (link_hash,))

    def get_link_stats(self, link):
        # Возвращаем количество кликов для заданной ссылки
        self.cursor.execute("SELECT clicks FROM links WHERE link = %s", (link,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return 0


tracker = TrafficTracker()
