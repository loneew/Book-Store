from DAO.interfaces.author_dao import AuthorDao
from models.author import Author
from connection.connection_pool import MySQLConnectionPool


class AuthorDaoImpl(AuthorDao):
    def __init__(self):
        self.cnx = MySQLConnectionPool().get_connection()

    def read_by_id(self, author_id: int):
        query = (f"SELECT * FROM author WHERE author_id={author_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = Author(*cursor.fetchone())
            result.print()
            cursor.close()
        except:
            print("Схоже, сталася помилка. Скоріш за все, автора з таким id не знайдено.")

    def add(self, author: Author):
        query = (f"INSERT INTO author(author_name, nationality) VALUES('{author.name}', '{author.nationality}')")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except:
            print("Схоже, сталася помилка. Спробуйте ще раз")

    def delete(self, author_id: int):
        query = (f"DELETE FROM author WHERE author_id={author_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except:
            print("Схоже, сталася помилка. Спробуйте ще раз")