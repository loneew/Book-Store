from service.reader import ReaderService


class ShowCatalog:
    def __init__(self):
        pass

    def execute(self):
        return ReaderService().catalog()
