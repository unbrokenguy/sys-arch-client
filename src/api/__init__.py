__all__ = ["ServerApi"]

import json

from api.factory import ApiFactory


class ServerApi:
    """
    Encapsulates Server api methods.
    """

    csrftoken = ""
    token = ""

    def __init__(self, url):
        self.factory = ApiFactory()
        self.factory.update_headers({"Accept": "application/json"})
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
            return self.api["create_data"](data=data)
        else:
            return self.api["create_data"](files=data["data"])
