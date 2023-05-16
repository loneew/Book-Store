class Author:
    def __init__(self, Id, Name, Nationality):
        self.id = Id
        self.name = Name
        self.nationality = Nationality

    def print(self):
        print(f" ID - {self.id}, Name - {self.name}, Nationality - {self.nationality}.")

    def get_all(self):
        return self.id, self.name, self.nationality

    def set_name(self, Name):
        self.name = Name

    def set_nationality(self, Nationality):
        self.nationality = Nationality
