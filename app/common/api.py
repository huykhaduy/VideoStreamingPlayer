import requests
# import os

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

    def post(self, endpoint, headers=None, data=None, files=None):
        headers = {**self.headers, **(headers if headers else {})}
        response = requests.post(self.base_url + endpoint, headers=headers, data=data, files=files)
        self.log(response)
        print("Response Content:", response.content)
        print("Response Headers:", response.headers)
        return response
    
    # def post(self, endpoint, headers=None, data=None, files=None):
    #     headers = {**self.headers, **(headers if headers else {})}

    #     # Generate boundary for multipart form data
    #     boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

    #     # Update content-type header with boundary
    #     headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'

    #     # Construct multipart form data payload
    #     payload = self.generate_multipart_payload(data, files, boundary)

    #     response = requests.post(self.base_url + endpoint, headers=headers, data=payload)
    #     self.log(response)
    #     print("Response Content:", response.content)
    #     print("Response Headers:", response.headers)
    #     return response

    # Get unique client token to verify which client is using the API
    def getClientToken(self):
        response = requests.get(self.base_url + "/client/token")
        self.log(response)
        return response

    def log(self, response):
        print(f"HTTP({response.status_code}): {response.url}")


    # def generate_multipart_payload(self, data, files, boundary):
    #     payload = b''
    #     # Add fields data
    #     if data:
    #         for key, value in data.items():
    #             payload += f'--{boundary}\r\n'.encode('utf-8')
    #             payload += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')
    #             payload += f'{value}\r\n'.encode('utf-8')

    #     # Add files data
    #     if files:
    #         for key, file_content in files.items():
    #             filename = os.path.basename(file_content.name)
    #             payload += f'--{boundary}\r\n'.encode('utf-8')
    #             payload += f'Content-Disposition: form-data; name="{key}"; filename="{filename}"\r\n'.encode('utf-8')
    #             payload += f'Content-Type: application/octet-stream\r\n\r\n'.encode('utf-8')
    #             payload += file_content.read()
    #             payload += b'\r\n'

    #     # Add final boundary
    #     payload += f'--{boundary}--\r\n'.encode('utf-8')

    #     return payload
