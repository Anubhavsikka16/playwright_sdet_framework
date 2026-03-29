from pages.dashboard_page import DashboardPage
from pages.transaction_page import TransactionPage

def test_user_flow(page, auth_token):

    # Inject token (skip login UI)
    page.add_init_script(f"""
        window.localStorage.setItem('token', '{auth_token}');
    """)

    page.goto("/dashboard")

    dashboard = DashboardPage(page)
    dashboard.open_transactions()

    transaction = TransactionPage(page)
    transaction.create_transaction("user1", "200")

    assert page.locator("text=Success").is_visible()