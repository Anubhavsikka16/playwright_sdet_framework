from core.config import  config
import allure   
from ui.pages.login_page import LoginPage
from validators.ui_validators import validate_dashboard_loaded
@allure.feature("Authentication")
@allure.story("User Login")
@allure.title("Verify user can login successfully")
def test_login_flow(page):
    login = LoginPage(page)

    login.open()
    login.login(config.USERNAME, config.PASSWORD)

    validate_dashboard_loaded(page)