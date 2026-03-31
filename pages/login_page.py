from pages.base_page import BasePage

class LoginPage(BasePage):

    def login(self, username, password):
        self.fill("#username", username)
        self.fill("#password", password)
        self.click("#login")