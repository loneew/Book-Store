from DAO.interfaces.book_dao import BookDao
from models.book import Book
from connection.connection_pool import MySQLConnectionPool


class BookDaoImpl(BookDao):
    def __init__(self):
        self.cnx = MySQLConnectionPool().get_connection()

    def read_by_id(self, book_id: int):
        query = (f"SELECT a.author_name, a.nationality, s.status_situation, b.idbook, b.key_words, b.title, "
                 f"b.amount_of_pages FROM book b INNER JOIN author a ON b.author_id = a.author_id INNER JOIN "
                 f"book_status s ON b.book_status = s.status_id WHERE idbook={book_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = Book(*cursor.fetchone())
            cursor.close()
            return result
        except:
            return None

    def check_book(self, book_id: int):
        query = (f"SELECT book_status FROM book WHERE idbook = {book_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result[0]
        except:
            return None

    def get_books(self):
        query = ("SELECT a.author_name, a.nationality, s.status_situation, b.idbook, b.key_words, b.title, "
                 "b.amount_of_pages FROM book b INNER JOIN author a ON b.author_id = a.author_id INNER JOIN "
                 "book_status s ON b.book_status = s.status_id;")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            books = []
            for i in range(len(result)):
                books.append(Book(*result[i]))
            return books
        except:
            raise Exception

    def get_books_with_id(self, user_id: int):
        query = (f"SELECT a.author_name, a.nationality, s.status_situation, b.idbook, b.key_words, b.title, "
                 f"b.amount_of_pages FROM order_book o INNER JOIN book b ON b.idbook = o.book_id INNER JOIN author a "
                 f"ON a.author_id = b.idbook INNER JOIN book_status s ON s.status_id = b.book_status INNER JOIN users "
                 f"u ON u.user_id = o.user_id WHERE o.user_id = {user_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            books = []
            for i in range(len(result)):
                books.append(Book(*result[i]))
            return books
        except:
            raise Exception

    def add(self, book: Book):
        query = f"INSERT INTO book(idbook, author_id, book_status, key_words, title, amount_of_pages) VALUES('{book.id}', '{book.author_id}', '{book.book_status}', '{book.key_words}', '{book.title}', '{book.amount_of_pages}') "
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except:
            raise Exception

    def delete(self, book_id: int):
        query = (f"DELETE FROM book WHERE idbook={book_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except:
            raise Exception
