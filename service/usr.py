import hashlib
from flask import session
from DAO.dao_impl.user_dao_impl import UserDaoImpl
from models.user import User


class UserService:
    def __init__(self):
        pass

    def register(self, name, surname, email, phone, password):
        user_table = UserDaoImpl()
        if user_table.read_by_email(email) is not None:
            return False, None, "Схоже, користувач з таким email вже існує. Спробуйте ще раз."
        if user_table.read_by_phone(phone) is not None:
            return False, None, "Схоже, користувач з таким номером телефону вже існує. Спробуйте ще раз."
        user = User.create(name, surname, email, phone, password)
        try:
            user_table.add(user)
            session['user'] = user.to_dict()
            return True, None, None
        except Exception as e:
            return False, None, str(e)

    def authorization(self, email, password):
        user_table = UserDaoImpl()
        user = user_table.read_by_email(email)
        if user is None:
            return False, None, "Схоже, ви ввели неправильну email адресу. Спробуйте ще раз."
        if user.get_pass() != hashlib.md5(password.encode()).hexdigest():
            return False, None, "Схоже, ви ввели неправильний пароль. Спробуйте ще раз."
        try:
            session['user'] = user.to_dict()
            if user.get_role() == 1:
                return True, 1, None
            if user.get_role() == 2:
                return True, 2, None
        except Exception as e:
            return False, None, str(e)
