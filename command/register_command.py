from service.usr import UserService


class Register:
    def __init__(self, Request):
        self.request = Request

    def execute(self):
        name = self.request.form['name']
        surname = self.request.form['surname']
        email = self.request.form['email']
        phone = self.request.form['phone']
        if self.request.form['password'] != self.request.form['confirm-password']:
            return False, None, "Схоже, ви ввели два різних паролі. Вони не співпадають."
        else:
            password = self.request.form['password']
        return UserService().register(name, surname, email, phone, password)

