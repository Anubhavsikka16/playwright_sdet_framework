from pages.base_page import BasePage
from components.sidebar import Sidebar

class DashboardPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.sidebar = Sidebar(page)

    def open_transactions(self):
        self.sidebar.go_to_transactions()