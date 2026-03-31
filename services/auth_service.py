from api.clients.api_client import APIClient
from core.config import Config
'''
Main responsibilities
create APIClient instance
send login request
assert login success
return token

'''

class AuthService:
    """
    Business logic layer for auth
    """

    def __init__(self):
        self.client = APIClient()

    def login(self):
        response = self.client.post("/login", {
            "username": Config.USERNAME,
            "password": Config.PASSWORD
        })

        assert response.status_code == 200

        token = response.json()["token"]

        self.client.set_token(token)

        return token