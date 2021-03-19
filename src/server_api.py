import json

import requests


class ServerApi:

    csrftoken = ""
    token = ""

    def __init__(self, url, auth_url):
        self.url = url + "/api"
        self.auth_url = auth_url
        self.client = requests.session()
        self.base_headers = {"accept": "application/json"}

    def login(self, email, password):
        credentials = {"email": email, "password": password}
        response = self.client.post(data=credentials, url=f"{self.auth_url}/auth/")
        self.token = json.loads(response.text)['token']
        self.base_headers.update({"Authorization": f"Token {self.token}"})

    def get_categories(self):
        response = self.client.get(f"{self.url}/category/")
        return response

    def get_category_data(self, category_id):
        response = self.client.get(f"{self.url}/category/{category_id}/")
        return response

    def get_data(self, file_id):
        response = self.client.get(
            url=f"{self.url}/data/{file_id}/",
            headers=self.base_headers,
        )
        return response

    def create_file(self, file):
        response = self.client.post(
            url=f"{self.url}/file/",
            headers=self.base_headers,
            data={},
            files=file,
        )
        return response

    def create_user_input(self, value):
        response = self.client.post(
            url=f"{self.url}/user_input/",
            headers=self.base_headers,
            data={"data": value},
        )
        return response
