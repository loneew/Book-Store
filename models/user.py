import hashlib


class User:
    def __init__(self, ID, Name, Surname, Email, Phone, Password, Role):
        self.id = ID
        self.name = Name
        self.surname = Surname
        self.email = Email
        self.phone = Phone
        self.password = Password
        # self.password = hashlib.md5(Password.encode()).hexdigest()
        self.role = Role

    @classmethod
    def create(cls, Name, Surname, Email, Phone, Password, ID=0, Role=1):
        return cls(ID, Name, Surname, Email, Phone, Password, Role)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'phone': self.phone,
            'password': self.password,
            'role': self.role
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['name'], data['surname'], data['email'], data['phone'], data['password'],
                   data['role'])

    def print(self):
        print(
            f" ID - {self.id}, Name and Surname - {self.name} {self.surname},\nemail - {self.email}, phone - {self.phone}, роль - {self.role}.")

    def get_pass(self):
        return self.password

    def get_role(self):
        return self.role

    def set_email(self, Email):
        self.email = Email

    def set_phone(self, Phone):
        self.phone = Phone
