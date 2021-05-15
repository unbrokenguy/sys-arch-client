import requests

from api.methods import ApiGetMethod, ApiPostMethod


class ApiFactory:
    """ApiMethod Factory"""

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
