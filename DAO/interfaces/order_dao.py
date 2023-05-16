from abc import ABC, abstractmethod


class OrderDao(ABC):
    @abstractmethod
    def create(self, obj: object):
        pass

