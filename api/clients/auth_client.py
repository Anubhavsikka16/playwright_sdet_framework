from api.clients.api_client import BaseClient

class AuthClient(BaseClient):
    def login(self, username, password):
        return self.post("/login", json={
            "username": username,
            "password": password
        })