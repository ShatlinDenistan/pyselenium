"""Test init and tear down methods"""

import pytest
import logging as logger
import timeit
import os
import shutil
from fnmatch import fnmatch
from automation.browser_strategy import BrowserSelector
from config.config import BASE_URL, BROWSER, LOG_SUMMARY_PATH
from datetime import datetime
from utils.scripter import Scripter


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")


@pytest.fixture(scope="class", autouse=True)
def test_setup(request):
    _browser = request.config.getoption("--browser")
    driver = BrowserSelector(_browser, BASE_URL).start()
    request.cls.driver = driver
    # Scripter(driver.page_source).generate_script()

    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def log_test_name():
    starttime = timeit.default_timer()
    testname = (
        os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
    ).upper()
    logger.info(f"{testname} STARTED")
    yield True
    time_taken = timeit.default_timer() - starttime
    formatted_time = "{:.2f}".format(time_taken)
    logger.info(f"{testname} COMPLETED IN: {formatted_time} SECONDS")


@pytest.fixture(scope="session", autouse=True)
def create_log_summary_file():
    # if os.getenv("ENVIRONMENT") != "DEV":
    #     return
    for dirpath, dirnames, filenames in os.walk("./logs/screenshots"):
        for file in filenames:
            if fnmatch(file, "*.png"):
                os.remove(os.path.join(dirpath, file))
    for dirpath, dirnames, filenames in os.walk("./logs/screenshots"):
        for name in dirnames:
            shutil.rmtree(os.path.join(dirpath, name))
    f = open(LOG_SUMMARY_PATH, "w")
    time = datetime.now().strftime("%d-%m-%Y %H:%S")
    f.write(f"{time}\tTests started\n")
    yield
    time = datetime.now().strftime("%d-%m-%Y %H:%S")
    f.write(f"{time}\tTests completed\n")
