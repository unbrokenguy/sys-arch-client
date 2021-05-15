from requests import RequestException

from api.methods.abstract import ApiMethod


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
            except RequestException as request_error:
                print(request_error)
            except KeyError as key_error:
                print(key_error)

        return function
