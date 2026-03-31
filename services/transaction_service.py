from api.clients.api_client import APIClient
'''
How it connects
uses APIClient
receives token during initialization
used in API validation or E2E validation

'''

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