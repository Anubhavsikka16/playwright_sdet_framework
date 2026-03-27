from playwright.sync_api import expect

def validate_dashboard_loaded(page):
    expect(page.locator("[data-test='sidenav']")).to_be_visible()