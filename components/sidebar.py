class Sidebar:

    def __init__(self, page):
        self.page = page

    def go_to_transactions(self):
        self.page.click("text=Transactions")