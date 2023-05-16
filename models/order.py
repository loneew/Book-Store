class Order:
    def __init__(self, User_id, Book_id, Status_id):
        self.user_id = User_id
        self.book_id = Book_id
        self.status_id = Status_id

    def print(self):
        print(self.user_id, self.book_id, self.status_id)