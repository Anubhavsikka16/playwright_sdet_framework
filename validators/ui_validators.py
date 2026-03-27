from playwright.sync_api import expect

def validate_dashboard_loaded(page):
    expect(page.locator("[data-test='sidenav-user-full-name']")).to_be_visible()