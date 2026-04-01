import pytest
import os
import allure
from playwright.sync_api import sync_playwright
from core.config import Config
from services.auth_service import AuthService


# =====================================================
# 🧠 HOOK: Capture Test Result (Required for failure handling)
# =====================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    This tells Pytest that this function is a hook.
    A hook is a special function Pytest calls automatically during test execution. 
    This hook runs after each phase of a test: setup, call (the test itself), and teardown.   
    Captures test execution result (pass/fail)
    Used later for screenshots, traces, etc.
    """
    outcome = yield # This hook runs after each phase of a test
    result = outcome.get_result() #This gets the actual test result object after Pytest finishes that phase.
    setattr(item, "rep_" + result.when, result) #This stores the result on the test item.


# =====================================================
# 🌐 BROWSER FIXTURE
# =====================================================
@pytest.fixture(scope="function")
def page(request): # test that asks for page gets a browser page object.
    #request is a special Pytest object that gives access to the current test context.
    """
    Browser fixture (enterprise-level):

    Features:
    - Env-driven config
    - Supports multiple browsers
    - Playwright tracing
    - Screenshot on failure
    - Allure integration
    """

    # 🔥 Select browser dynamically
    browser_type = getattr(Config, "BROWSER", "chromium")
    #getattr(object, "attribute_name", default_value)
    #“Get value of this attribute from object — if not found, use default”

    with sync_playwright() as p: #starts Playwright context and p is the Playwright object that gives access to browsers.

        browser_launcher = getattr(p, browser_type) #p.firefox or p.chromium or p.webkit based on config.

        browser = browser_launcher.launch(
            headless=Config.HEADLESS
        )

        context = browser.new_context(
            base_url=Config.BASE_URL
        )

        # 🔥 Start tracing (always)
        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()
        '''This opens a new browser tab/page inside the context.

            Your tests use this page object to:

                go to URLs
                click buttons
                fill forms
                validate text'''

        yield page
        '''
            It gives control to the test function.

            The test runs using this page.

            After the test completes, Pytest comes back to the fixture and runs the cleanup code below the yield.
        
        
        '''
        

        # =====================================================
        # 🔥 FAILURE HANDLING
        # =====================================================
        test_failed = (
            hasattr(request.node, "rep_call") and #Checks whether the rep_call result exists.
            request.node.rep_call.failed #You only want to save screenshot and trace when the test fails, not on every passing test.
        )

        if test_failed:
            # 📸 Screenshot
            screenshot = page.screenshot()

            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # 📦 Trace path
            trace_dir = "reports/traces"
            os.makedirs(trace_dir, exist_ok=True)

            trace_path = os.path.join(
                trace_dir,
                f"{request.node.name}.zip"
            )

            # Save trace
            context.tracing.stop(path=trace_path)

            # Attach trace
            if os.path.exists(trace_path): # if file exists, attach to Allure report
                with open(trace_path, "rb") as f: #opens in binary mode since it's a zip file
                    allure.attach(
                        f.read(),
                        name="Playwright Trace",
                        attachment_type=allure.attachment_type.ZIP
                    )
        else:
            # Stop tracing without saving (optimization)
            context.tracing.stop()

        # Cleanup
        context.close()
        browser.close()


# =====================================================
# 🔐 AUTH FIXTURE
# =====================================================
@pytest.fixture(scope="function")
def auth_token():
    """
    Authentication fixture:
    - Calls AuthService
    - Returns JWT token
    """

    service = AuthService()
    token = service.login()

    assert token, "Auth token is None!"

    return token


# =====================================================
# 🌐 API CLIENT FIXTURE
# =====================================================
@pytest.fixture(scope="function")
def api_client(auth_token):
    """
    API client fixture:
    - Injects auth token
    - Ready for API testing
    """

    from api.clients.api_client import APIClient  # ✅ corrected import

    client = APIClient()
    client.set_token(auth_token)

    return client


# =====================================================
# 🗄️ DATABASE FIXTURE
# =====================================================
# @pytest.fixture(scope="function")
# def db():
#     """
#     Database fixture:
#     - Opens DB connection
#     - Closes after test
#     """

#     from core.db_client import DBClient

#     db_client = DBClient()

#     yield db_client

#     db_client.close()


# =====================================================
# ⚙️ OPTIONAL: CLI OPTIONS (ADVANCED)
# =====================================================
def pytest_addoption(parser):
    """
    Adds CLI options:
    Example:
        pytest --env=prod --browser=chromium
    """
    parser.addoption("--env", action="store", default="prod")
    parser.addoption("--browser", action="store", default="chromium")


@pytest.fixture(scope="session", autouse=True)
def setup_env(request):
    """
    Set environment dynamically from CLI
    """
    os.environ["ENV"] = request.config.getoption("--env")
    os.environ["BROWSER"] = request.config.getoption("--browser")