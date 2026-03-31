import requests
from core.config import Config as config
#“APIClient is a reusable wrapper around the Requests library. 
# It standardizes request handling, headers, and authentication across the framework.”
class APIClient:
    """
    What it handles
        --> GET requests
        --> POST requests
        --> authorization token
        --> JSON headers
    """

    def __init__(self):
        self.base_url = config.API_BASE_URL

        if not self.base_url:
            raise ValueError("API_BASE_URL is NOT set in environment!")

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