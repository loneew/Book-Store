from flask import session, app
from models.user import User
from service.reader import ReaderService
app.secret_key = 'user'


class ShowBooks:
    def __init__(self):
        pass

    def execute(self):
        user_data = session.get('user')
        user = User.from_dict(user_data)
        return ReaderService().show_books(user.id)

