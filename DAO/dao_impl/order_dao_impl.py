from DAO.interfaces.order_dao import OrderDao
from models.order import Order
from connection.connection_pool import MySQLConnectionPool


class OrderDaoImpl(OrderDao):
    def __init__(self):
        self.cnx = MySQLConnectionPool().get_connection()

    def create(self, order: Order):
        query1 = f"INSERT INTO order_book(user_id, book_id, status_id, date_created) VALUES('{order.user_id}', '{order.book_id}', '{order.status_id}', CURRENT_DATE()) "
        query2 = f"UPDATE book SET book_status = 2 WHERE idbook = {order.book_id}"
        conn = self.cnx.get_connection()
        cursor = conn.cursor()
        try:
            conn.autocommit = False
            cursor.execute(query1)
            cursor.execute(query2)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.autocommit = True
            cursor.close()
            conn.close()

