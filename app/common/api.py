import requests


class APIInterceptor:
    def __init__(self, base_url="", header=None):
        if header is None:
            header = {}
        self.base_url = base_url
        if self.base_url == "":
            self.base_url += "http://127.0.0.1:8000/api/"
        else:
            self.base_url += "/"
        self.headers = header

    def get(self, endpoint, headers=None, params=None):
        headers = {**self.headers, **(headers if headers else {})}
        response = requests.get(self.base_url + endpoint, headers=headers, params=params)
        self.log(response)
        return response

    def post(self, endpoint, headers=None, data=None):
        headers = {**self.headers, **(headers if headers else {})}
        response = requests.post(self.base_url + endpoint, headers=headers, data=data)
        self.log(response)
        return response

    # Get unique client token to verify which client is using the API
    def getClientToken(self):
        response = requests.get(self.base_url + "/client/token")
        self.log(response)
        return response

    def log(self, response):
        print(f"HTTP({response.status_code}): {response.url}")


