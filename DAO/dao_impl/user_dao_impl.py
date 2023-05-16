import hashlib
from connection.connection_pool import MySQLConnectionPool
from models.user import User
from DAO.interfaces.user_dao import UserDao


class UserDaoImpl(UserDao):
    def __init__(self):
        self.cnx = MySQLConnectionPool().get_connection()

    def read_by_id(self, user_id: int):
        query = (f"SELECT * FROM users WHERE user_id={user_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = User(*cursor.fetchone())
            cursor.close()
            return result
        except:
            return None

    def read_by_email(self, email: str):
        query = "SELECT * FROM users WHERE users_email = '{}'".format(email)
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = User(*cursor.fetchone())
            # result.print()
            cursor.close()
            return result
        except:
            return None

    def read_by_phone(self, phone: str):
        query = "SELECT * FROM users WHERE user_phone = '{}'".format(phone)
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            result = User(*cursor.fetchone())
            # result.print()
            cursor.close()
            return result
        except:
            return None

    def add(self, user: User):
        query = f"INSERT INTO users(user_name, user_surname, users_email, user_phone, user_password, user_role_id) VALUES('{user.name}', '{user.surname}', '{user.email}', '{user.phone}', '{hashlib.md5(user.password.encode()).hexdigest()}', '{user.role}') "
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except:
            raise Exception()

    def delete(self, user_id: int):
        query = (f"DELETE FROM users WHERE user_id={user_id}")
        try:
            conn = self.cnx.get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
        except:
            raise Exception()
