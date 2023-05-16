from mysql.connector import pooling
import mysql.connector


class MySQLConnectionPool:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'password',
            'host': 'localhost',
            'database': 'library',
            'pool_name': 'mypool',
            'pool_size': 10
        }

    def get_connection(self):
        try:
            connection = mysql.connector.pooling.MySQLConnectionPool(**self.config)
        except mysql.connector.Error as error:
            print(f' Помилка. Не вдалося з`єдання із БД. Код помилки:\n{error}\n')
            connection = None
            exit(1)
        return connection
