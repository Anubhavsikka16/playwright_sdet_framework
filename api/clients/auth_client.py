from api.api_client import APIClient
from core.config import Config

class AuthService:
    """
    “AuthService contains the business logic for authentication, so tests stay clean and do not need to know request details.”
    """

    def __init__(self):
        self.client = APIClient()

    def login_and_get_token(self):
        response = self.client.post("/signin", {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        })

        assert response.status_code == 200

        token = response.json()["token"]

        # Set token globally
        self.client.set_token(token)

        return token