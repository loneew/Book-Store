from abc import ABC, abstractmethod


class BookDao(ABC):
    @abstractmethod
    def read_by_id(self, obj: object):
        pass

    @abstractmethod
    def check_book(self, obj: object):
        pass

    @abstractmethod
    def get_books(self):
        pass

    @abstractmethod
    def get_books_with_id(self, obj: object):
        pass

    @abstractmethod
    def add(self, obj: object):
        pass

    @abstractmethod
    def delete(self, obj: object):
        pass
