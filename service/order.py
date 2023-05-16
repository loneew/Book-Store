from DAO.dao_impl.book_dao_impl import BookDaoImpl
from DAO.dao_impl.order_dao_impl import OrderDaoImpl
from models.order import Order


class OrderService:
    def __init__(self):
        pass

    def make_order(self, book_id, user_id):
        book_table = BookDaoImpl()
        if book_table.read_by_id(book_id) is None:
            return False, None, "Схоже, ви Ввели ID книжки, якої в нас немає"
        if book_table.check_book(book_id) == 2:
            return False, None, "Схоже, ви Ввели ID книжки, яку вже хтось взяв почитати"
        order = Order(user_id, book_id, 1)
        try:
            order_table = OrderDaoImpl()
            order_table.create(order)
            return True, None, "Ви успішно замовили книжку."
        except Exception as e:
            return False, None, str(e)

