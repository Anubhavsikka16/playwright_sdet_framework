import pytest
from playwright.sync_api import sync_playwright
from core.config import Config

@pytest.fixture
def page(request):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS)

        context = browser.new_context(base_url=Config.BASE_URL)

        context.tracing.start(
            screenshots=True,
            snapshots=True,
            sources=True
        )

        page = context.new_page()

        yield page

        # Check test result
        if request.node.rep_call.failed:
            trace_path = f"reports/traces/{request.node.name}.zip"

            context.tracing.stop(path=trace_path)
        else:
            context.tracing.stop()

        context.close()
        browser.close()