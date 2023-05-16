from service.usr import UserService


class Authorization:
    def __init__(self, Request):
        self.request = Request

    def execute(self):
        email = self.request.form['email']
        password = self.request.form['password']
        return UserService().authorization(email, password)
