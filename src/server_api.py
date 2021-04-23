import json
from abc import ABC, abstractmethod
from requests.exceptions import RequestException
import requests


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


class ApiGetMethod(ApiMethod):
    """
    Decorator of requests.get method.
    ApiMethod Implementation
    """

    def __init__(self, url, client):
        super().__init__(url, client)
        self.method = self.client.get

    def request(self):
        def function(*args, **kwargs):
            try:
                return self.method(
                    url=self.url,
                    headers=kwargs.get("headers") or {},
                )
            except RequestException or KeyError as e:
                print(e)

        return function


class ApiPostMethod(ApiMethod):
    """
    Decorator of requests.post method.
    ApiMethod Implementation.
    """

    def __init__(self, url, client):
        super().__init__(url, client)
        self.method = self.client.post

    def request(self):
        def function(*args, **kwargs):
            try:
                return self.method(
                    url=self.url,
                    headers=kwargs.get("headers") or {},
                    data=kwargs.get("data") or {},
                    files=kwargs.get("files") or {},
                )
            except RequestException or KeyError as e:
                print(e)

        return function


class ApiFactory:
    def __init__(self):
        self.client = requests.session()
        self.methods = {"GET": ApiGetMethod, "POST": ApiPostMethod}

    def make(self, *args, **kwargs):
        """Makes the ApiMethod that makes the request to the api
        Args:
            kwargs: method, url, headers, data, files
        Returns:
            function: pointer to a function
        Raises:
            RequestException, KeyError
        """
        try:
            return self.methods[args[0]](url=args[1], client=self.client).request()
        except KeyError as e:
            print(e)

    def update_headers(self, headers):
        self.client.headers.update(headers)


class ServerApi:

    csrftoken = ""
    token = ""

    def __init__(self, url):
        self.factory = ApiFactory()
        self.factory.update_headers({"accept": "application/json"})
        self.api = {
            "login": self.factory.make("POST", f"{url}/auth/sign_in/"),
            "get_categories": self.factory.make("GET", f"{url}/category/"),
            "get_category": lambda pk: self.factory.make("GET", f"{url}/category/{pk}/"),
            "get_data": lambda pk: self.factory.make("GET", f"{url}/data/{pk}/"),
            "create_data": self.factory.make("POST", f"{url}/data/"),
        }

    def login(self, email, password):
        """Sign in method
        POST request "<api>/auth/sign_in/"
        Args:
            email: user email.
            password: user password.
        """
        response = self.api["login"](data={"email": email, "password": password})
        if response.status_code != 200:
            raise Exception("Неверный логин или пароль")
        self.token = json.loads(response.text)["auth_token"]
        self.factory.update_headers({"Authorization": f"Token {self.token}"})

    def get_categories(self):
        """Get list of categories.
        GET request "<api>/category/"
        Returns:
            Response from server.
        """
        return self.api["get_categories"]()

    def get_category_data(self, category_id: int):
        """Retrieve category from server.
        GET request "<api>/category/{pk}/"
        """
        return self.api["get_category"](category_id)()

    def get_data(self, data_id):
        """Retrieve data from server.
        GET request "<api>/data/{pk}/"
        """
        return self.api["get_data"](data_id)()

    def create_data(self, data):
        """Create data on server.
        POST request "<api>/data/"
        """
        if isinstance(data["data"], str):
            return self.api["create_data"](data=data["data"])
        else:
            return self.api["create_data"](files=data["data"])
