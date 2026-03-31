def test_login(page):
#Simulates real user actions in browser
    page.goto("/signin")
    page.fill("#username", "anubhav123")
    page.fill("#password", "secret")
    page.click("button[data-test='signin-submit']")

    assert "dashboard" in page.url