from abc import abstractmethod, ABC


class ApiMethod(ABC):
    """
    Interface for requests
    """

    def __init__(self, url, client):
        self.url = url
        self.client = client

    @abstractmethod
    def request(self):
        def function(*args, **kwargs):
            pass

        return function
