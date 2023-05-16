class Book:
    #def __init__(self, Id, Author, Key_words, Title, Amount_of_pages, Book_status=1):
    #    self.id = Id
    #    if isinstance(Author, int):
    #        self.author_id = Author
    #   else:
    #        self.author_id = Author.id
    #   self.book_status = Book_status
    #    self.key_words = Key_words
    #    self.title = Title
    #    self.amount_of_pages = Amount_of_pages
    def __init__(self, Author_Name, Author_nationality, Status, ID, Key_words, Title, Amount_of_pages):
        self.id = ID
        self.author_name = Author_Name
        self.author_nationality = Author_nationality
        self.status = Status
        self.key_words = Key_words
        self.title = Title
        self.amount_of_pages = Amount_of_pages

    def print(self):
        print(self.author_name, self.author_nationality, self.status, self.key_words, self.title, self.amount_of_pages)
    #    if self.book_status == 1:
    #        print(
    #            f" Місце книжки на полці - {self.id}, ID автора книжки - {self.author_id}, Статус - доступна, Назва - '{self.title}'.")
    #    else:
    #        print(
    #            f" Місце книжки на полці - {self.id}, ID автора книжки - {self.author_id}, Статус - не доступна, "
    #            f"Назва - {self.title}")

    #def get_all(self):
    #    return self.id, self.author_id, self.book_status, self.key_words, self.title, self.amount_of_pages

    #def set_book_status_id(self, Book_status):
    #    self.book_status = Book_status
