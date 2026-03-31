import pymysql
from core.config import Config
#Used by the db fixture in conftest.py
class DBClient:
    """
    Database connection handler
    """

    def __init__(self):
        self.connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

    def execute_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

    def close(self):
        self.connection.close()