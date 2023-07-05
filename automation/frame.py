import logging as logger
from automation.selenium_base import SeleniumBase
from automation.wait_times import DEFAULT, SHORT
from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchFrameException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from typing import Union
from selenium.webdriver.remote.webelement import WebElement


class Frame(SeleniumBase):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.info("Frame  initialized")

    def select_frame(self, frame_reference):
        try:
            self.driver.switch_to.frame(frame_reference)
            return True
        except (TimeoutException, NoSuchFrameException, NoSuchElementException):
            return False

    def unselect_frame(self):
        self.driver.switch_to.default_content()

    def current_frame_should_contain(self, text: str):
        """Verifies that the current frame contains ``text``."""
        if not self.is_text_present(text):
            raise AssertionError(
                f"Frame should have contained text '{text}' but did not."
            )
        logger.info(f"Current frame contains text '{text}'.")

    def current_frame_should_not_contain(self, text: str):
        """Verifies that the current frame does not contain ``text``."""
        if self.is_text_present(text):
            raise AssertionError(
                f"Frame should not have contained text '{text}' but it did."
            )
        logger.info(f"Current frame did not contain text '{text}'.")

    def frame_should_contain(self, locator: Union[WebElement, str], text: str):
        """Verifies that frame identified by ``locator`` contains ``text``."""
        if not self._frame_contains(locator, text):
            raise AssertionError(
                f"Frame '{locator}' should have contained text '{text}' but did not."
            )
        logger.info(f"Frame '{locator}' contains text '{text}'.")

    def _frame_contains(self, locator: Union[WebElement, str], text: str):
        element = self.get_element(locator)
        self.driver.switch_to.frame(element)
        logger.info(f"Searching for text from frame '{locator}'.")
        found = self.is_text_present(text)
        self.driver.switch_to.default_content()
        return found
