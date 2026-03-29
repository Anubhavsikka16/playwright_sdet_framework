import requests
from core.config import Config as config

class APIClient:
    """
    Handles all HTTP calls
    """

    def __init__(self):
        self.base_url = config.API_URL
        self.token = None

    def set_token(self, token):
        self.token = token

    def headers(self):
        headers = {}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def post(self, endpoint, data):
        return requests.post(
            f"{self.base_url}{endpoint}",
            json=data,
            headers=self.headers()
        )

    def get(self, endpoint):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=self.headers()
        )