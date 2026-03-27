from playwright.sync_api import expect
from core.config import config

class LoginPage():
    
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Sign in")
        
    def open(self):
        self.page.goto(config.BASE_URL + "/signin")
        
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        expect(self.login_button).to_be_enabled()
        self.login_button.click()