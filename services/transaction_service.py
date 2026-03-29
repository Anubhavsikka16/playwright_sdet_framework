from api.clients.api_client import APIClient

class TransactionService:

    def __init__(self):
        self.client = APIClient()

    def get_transactions(self):
        response = self.client.get("/transactions")
        return response.json()

    def create_transaction(self, amount):
        return self.client.post("/transactions", {
            "amount": amount
        })