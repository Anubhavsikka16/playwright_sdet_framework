import pytest
import os
import shutil
import allure
from core.config import config

# ==============================
# 📁 PATH CONFIG- CREATE FOLDERS
# ==============================
ALLURE_RESULTS_DIR = "reports/allure-results"
TRACE_DIR = "reports/traces"
VIDEO_DIR = "reports/videos"

os.makedirs(TRACE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


# ==============================
# 🔥 CLEAN ALLURE BEFORE RUN- Deletes old Allure report and Creates a new empty one
# ==============================
def pytest_sessionstart(session):
    if os.path.exists(ALLURE_RESULTS_DIR):
        shutil.rmtree(ALLURE_RESULTS_DIR)
    '''Checks whether reports/allure-results already exists.
        If it exists, deletes it completely.
        Recreates the folder fresh.
    '''

    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)


# ==============================
# 🎥 CONTEXT OPTIONS (VIDEO)
# ==============================
@pytest.fixture(scope="function")
def context_options(): # This fixture provides video recording options for each test context and runs before each test
    return {
        "record_video_dir": VIDEO_DIR,
        "record_video_size": {"width": 1280, "height": 720},
    }


# ==============================
# 🧠 START TRACE
# ==============================
@pytest.fixture(autouse=True)
def start_trace(context):
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield


# ==============================
# ⚙️ CLI OPTIONS
# ==============================
def pytest_addoption(parser):
    #👉 You are adding a custom button/setting for your test run and will allow to run --headless command in terminal
    parser.addoption("--headless", action="store", default=None)


@pytest.fixture(autouse=True)
def override_config(request):
    #Get the value of --headless from command line and override config.HEADLESS if provided
    headless = request.config.getoption("--headless")

    if headless is not None:
        config.HEADLESS = headless.lower() == "true"


# ==============================
# 🧪 TEST REPORT HOOK
# ==============================
#Run this code after every test
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield #This allows the test to run and then captures the result after it finishes
    rep = outcome.get_result() #Get the test result (pass/fail/skip) and other info

    setattr(item, "rep_" + rep.when, rep)#Store the test result in the test item for later use (e.g., rep_call for the main test execution phase)

    # Only act after test execution
    #it tell which phase, i.e. setup, call, teardown. We only want to do our logic after the main test execution (call)
    if rep.when != "call":  #Only care about actual test result and ignore setup/teardown phases
        return

    page = item.funcargs.get("page") #Get browser page if test used it
    context = item.funcargs.get("context") #Get browser session if available

    # 🔥 Safe unique test name (parallel-friendly)
    test_name = item.nodeid.replace("/", "_").replace("::", "_") #Create a unique test name by replacing slashes and colons with underscores (e.g., tests/test_example.py::test_case -> tests_test_example_py_test_case)

    trace_path = f"{TRACE_DIR}/{test_name}.zip"

    # ==============================
    # 🧠 STOP TRACE (ALWAYS)
    # ==============================
    if context:
        try:
            context.tracing.stop(path=trace_path)
        except Exception as e:
            print(f"Trace stop failed: {e}")

    # ==============================
    # ❌ HANDLE FAILURE ONLY
    # ==============================
    if not rep.failed or not page: #Stop here if test did NOT fail OR browser page is not available
        return #not rep.failed = True, function stops

    # 📸 Screenshot
    try:
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except Exception as e:
        print(f"Screenshot failed: {e}")

    # 🧠 Attach Trace
    try:
        if os.path.exists(trace_path):
            with open(trace_path, "rb") as f:
                allure.attach(
                    f.read(),
                    name="trace",
                    attachment_type=allure.attachment_type.ZIP
                )
    except Exception as e:
        print(f"Trace attach failed: {e}")

    # 🎥 Attach Video (IMPORTANT: video available AFTER test ends)
    try:
        video = page.video
        if video:
            video_path = video.path()
            if os.path.exists(video_path):
                with open(video_path, "rb") as f:
                    allure.attach(
                        f.read(),
                        name="video",
                        attachment_type=allure.attachment_type.WEBM
                    )
    except Exception as e:
        print(f"Video attach failed: {e}")
        
'''Start pytest
↓
Clean old report
↓
Start test
↓
Start trace + video
↓
Run test steps
↓
Test ends
↓
Stop trace
↓
IF FAILED:
   → Screenshot
   → Trace
   → Video
↓
Show in Allure

'''
