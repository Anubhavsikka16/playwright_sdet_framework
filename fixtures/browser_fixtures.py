import pytest
from playwright.sync_api import sync_playwright
from requests import request
from core.config import config

import pytest
import os
import allure
from playwright.sync_api import sync_playwright
from core.config import config

# 🔥 Ensure folders exist
TRACE_DIR = "reports/traces"
VIDEO_DIR = "reports/videos"

os.makedirs(TRACE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


@pytest.fixture
def page(request):
    with sync_playwright() as p:

        # 🔥 Browser selection
        browser_type = config.BROWSER

        if browser_type == "chromium":
            browser = p.chromium.launch(headless=config.HEADLESS)
        elif browser_type == "firefox":
            browser = p.firefox.launch(headless=config.HEADLESS)
        elif browser_type == "webkit":
            browser = p.webkit.launch(headless=config.HEADLESS)
        else:
            raise ValueError(f"Unsupported browser: {browser_type}")

        # 🔥 Context with video
        context = browser.new_context(
            base_url=config.BASE_URL,
            record_video_dir=VIDEO_DIR
        )

        # 🔥 Start tracing
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page = context.new_page()

        yield page

        # 🔥 Unique name for parallel safety
        test_name = request.node.name.replace("/", "_")
        trace_path = f"{TRACE_DIR}/{test_name}.zip"

        # 🔥 Stop trace
        context.tracing.stop(path=trace_path)

        # 🔥 Attach ONLY on failure
        if request.node.rep_call.failed:

            # Screenshot
            screenshot = page.screenshot()
            allure.attach(
                screenshot,
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # Trace
            if os.path.exists(trace_path):
                with open(trace_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="trace",
                        attachment_type=allure.attachment_type.ZIP
                    )

            # Video
            try:
                video_path = page.video.path()
                if os.path.exists(video_path):
                    with open(video_path, "rb") as f:
                        allure.attach(
                            f.read(),
                            name="video",
                            attachment_type=allure.attachment_type.WEBM
                        )
            except:
                pass

        context.close()
        browser.close()