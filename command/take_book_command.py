from flask import app, session
from models.user import User
from service.order import OrderService
app.secret_key = 'user'


class TakeBook:
    def __init__(self, Request):
        self.request = Request

    def execute(self):
        book_id = self.request.form['id']
        if int(book_id) < 1:
            return False, None, "Ви ввели неіснуючий ID книжки"
        else:
            user_data = session.get('user')
            user = User.from_dict(user_data)
            return OrderService().make_order(book_id, user.id)
