from flask import session, render_template, app
from models.user import User

app.secret_key = 'user'


class Reader:
    def __init__(self):
        self.proc = 1

    def execute(self):
        user_data = session.get('user')
        user = User.from_dict(user_data)
        return render_template("profile.html", name=user.name, surname=user.surname)
