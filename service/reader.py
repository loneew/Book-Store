from DAO.dao_impl.book_dao_impl import BookDaoImpl


class ReaderService:
    def __init__(self):
        pass

    def catalog(self):
        book_table = BookDaoImpl()
        try:
            result = book_table.get_books()
            return True, result, None
        except Exception as e:
            return False, None, str(e)

    def show_books(self, user_id):
        book_table = BookDaoImpl()
        try:
            result = book_table.get_books_with_id(user_id)
            return True, result, None
        except Exception as e:
            return False, None, str(e)



