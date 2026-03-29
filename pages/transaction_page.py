from pages.base_page import BasePage

class TransactionPage(BasePage):

    USER = "#user"
    AMOUNT = "#amount"
    SUBMIT = "#submit"

    def create_transaction(self, user, amount):
        self.fill(self.USER, user)
        self.fill(self.AMOUNT, amount)
        self.click(self.SUBMIT)