class DashboardPage:
    def __init__(self, page):
        self.page = page

    def is_loaded(self):
        return self.page.locator("[data-test='sidenav']").is_visible()

    def click_new_transaction(self):
        self.page.get_by_role("button", name="New").click()