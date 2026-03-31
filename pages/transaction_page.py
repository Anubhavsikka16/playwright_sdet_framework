from pages.base_page import BasePage

class TransactionPage(BasePage):

    def create_transaction(self, user, amount):
        self.fill("#user", user)
        self.fill("#amount", amount)
        self.click("#submit")