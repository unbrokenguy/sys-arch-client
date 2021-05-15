from requests import RequestException

from api.methods import ApiMethod


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
            except RequestException as request_error:
                print(request_error)
            except KeyError as key_error:
                print(key_error)

        return function
