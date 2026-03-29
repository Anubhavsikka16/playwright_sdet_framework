import pytest
import allure

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    setattr(item, "rep_" + result.when, result)
    if result.when == "call":
        page = item.funcargs.get("page")

        if page:
            screenshot = page.screenshot()

            if result.failed:
                # Attach screenshot on failure
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )