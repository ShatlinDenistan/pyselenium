import contextlib
import os
import logging as logger
import random
from automation.selenium_base import SeleniumBase
from selenium.webdriver.remote.webdriver import WebDriver


class Screenshot(SeleniumBase):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_image_path(self, message):
        test_class = os.environ.get("PYTEST_CURRENT_TEST").split(":")[2]
        test_name = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
        with contextlib.suppress(Exception):
            folder = "./logs/screenshots"
            os.mkdir(folder)
        with contextlib.suppress(Exception):
            folder = f"{folder}/{test_class}"
            os.mkdir(folder)
        with contextlib.suppress(Exception):
            folder = f"{folder}/{test_name}"
            os.mkdir(folder)
        if message is not None:
            image_path = f"{folder}/{message}.png"
        else:
            image_path = f"{folder}/{random.randint(1,10000000)}.png"

        logger.info(f" screenshot for {image_path.lower()}")
        return image_path.lower()

    def take_screenshot(self, message=None):
        try:
            path = self.get_image_path(message)
            self.driver.save_screenshot(path)
        except Exception:
            logger.info(f"Failed to take screenshot for {message}")
