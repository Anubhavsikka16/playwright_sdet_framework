import pytest
from playwright.sync_api import sync_playwright
from core.config import Config
from services.auth_service import AuthService
import allure
import os

# ================================
# 🧠 HOOK: Capture Test Result
# ================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach test result (pass/fail) to test node
    Used by fixtures for conditional logic
    """
    outcome = yield
    result = outcome.get_result()

    setattr(item, "rep_" + result.when, result)


# ================================
# 🌐 BROWSER FIXTURE (CORE)
# ================================
@pytest.fixture(scope="function")
def page(request):
    """
    Enterprise browser fixture:
    - Env-driven
    - Tracing enabled
    - Allure integrated
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS)

        context = browser.new_context(
            base_url=Config.BASE_URL
        )

        # Start tracing
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()

        yield page

        # =========================
        # 🔥 FAILURE HANDLING
        # =========================
        if request.node.rep_call.failed:

            # 📸 Screenshot
            screenshot = page.screenshot()

            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # 📦 Save trace
            trace_path = f"reports/traces/{request.node.name}.zip"

            context.tracing.stop(path=trace_path)

            # Attach trace to Allure
            if os.path.exists(trace_path):
                with open(trace_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="Playwright Trace",
                        attachment_type=allure.attachment_type.ZIP
                    )

        else:
            context.tracing.stop()

        context.close()
        browser.close()


# ================================
# 🔐 AUTH FIXTURE
# ================================
@pytest.fixture(scope="function")
def auth_token():
    """
    Central authentication fixture
    """
    service = AuthService()
    return service.login()


# ================================
# 🌐 API CLIENT FIXTURE
# ================================
@pytest.fixture(scope="function")
def api_client(auth_token):
    """
    API client with injected token
    """
    from api.clients.api_client import APIClient

    client = APIClient()
    client.set_token(auth_token)

    return client


# ================================
# 🗄️ DATABASE FIXTURE
# ================================
@pytest.fixture(scope="function")
def db():
    """
    Database connection fixture
    """
    from core.db_client import DBClient

    db_client = DBClient()
    yield db_client
    db_client.close()