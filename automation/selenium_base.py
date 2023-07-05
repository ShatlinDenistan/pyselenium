import datetime
import logging as logger
import time
from typing import List, Optional, Tuple, Union

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from automation.error import (
    ElementNotFoundException,
    ElementNotVisibleException,
    NotValidLocatorException,
)
from utils.common import type_converter
from automation.wait_times import DEFAULT, SHORT
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumBase:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.info("Selenium Base initialized")

    locator_types = {
        "css": By.CSS_SELECTOR,
        "id": By.ID,
        "name": By.NAME,
        "xpath": By.XPATH,
        "x": By.XPATH,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT,
        "tag": By.TAG_NAME,
        "class": By.CLASS_NAME,
    }

    def get_date_string(self):
        """Getting a date string to use for naming files"""
        return datetime.datetime.now().strftime("%y%m%d%H%M%S")

    def go_to(self, url):
        self.driver.get(url)

    def go_back(self):
        self.driver.back()

    def reload_page(self):
        self.driver.refresh()

    def get_source(self) -> str:
        """Returns the entire HTML source of the current page or frame."""
        return self.driver.page_source

    def get_title(self) -> str:
        """Returns the title of the current page."""
        return self.driver.title

    def get_location(self) -> str:
        """Returns the current browser window URL."""
        return self.driver.current_url

    # region element finder methods

    def get_text(self, locator: Union[WebElement, str]) -> WebElement:
        """
        get text from input box
        :param: None
        :return: text from webElement
        """
        element = self.get_element(locator)
        return element.get_attribute("innerText")

    def get_elements(self, locator, timeout=DEFAULT):
        locator = self._get_locator_tuple(locator)
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return self.driver.find_elements(locator[0], locator[1])
        except Exception as exception:
            self.handle_exception(
                exception, f"Exception at get_elements for: {locator}"
            )

    def get_child_elements(self, parentlocator, locator):
        try:
            parentelement = self.get_element(parentlocator)
            locator = self._get_locator_tuple(locator)
            return parentelement.find_elements(locator[0], locator[1])
        except NoSuchElementException as exception:
            self.handle_exception(
                exception, f"NoSuchElementException: get_elements: {locator}"
            )
        except TimeoutException as exception:
            self.handle_exception(
                exception, f"TimeoutException: get_elements: {locator}"
            )
        except StaleElementReferenceException as exception:
            self.handle_exception(
                exception,
                f"StaleElementReferenceException: get_child_elements: {locator}",
            )

    def get_element(self, locator, timeout=DEFAULT) -> WebElement:
        if isinstance(locator, WebElement):
            return locator

        locator = self._get_locator_tuple(locator)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except (
            StaleElementReferenceException,
            NoSuchElementException,
            TimeoutException,
        ) as e:
            raise ElementNotFoundException(
                "An exception of type "
                + type(e).__name__
                + " occurred. With Element -: "
                + " - locator: ("
                + locator[0]
                + ", "
                + locator[1]
                + ")"
            ) from e

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except (
            StaleElementReferenceException,
            NoSuchElementException,
            TimeoutException,
        ) as e:
            raise ElementNotVisibleException(
                "An exception of type "
                + type(e).__name__
                + " occurred. With Element -: "
                + " - locator: ("
                + locator[0]
                + ", "
                + locator[1]
                + ")"
            ) from e

        return element

    def _get_locator_tuple(self, locator: str) -> tuple:
        if locator_given := [
            x for x in SeleniumBase.locator_types.keys() if locator.startswith(x)
        ]:
            locator_split = locator.split("=", 1)
            identify_by = locator_split[0].strip().lower()
            locator = locator_split[1].strip().lower()
        else:
            identify_by = "xpath"

        if identify_by not in SeleniumBase.locator_types:
            raise NotValidLocatorException(
                f"""An exception of type
                NotValidLocatorException
                occurred. With Element -:
                + {locator}"""
            )
        by = SeleniumBase.locator_types[identify_by]
        return (by, locator)

    # endregion

    # region wait methods

    def wait_until_page_is_completely_loaded(self):
        WebDriverWait(self.driver, SHORT).until(
            lambda wd: self.driver.execute_script("return document.readyState")
            == "complete",
            "Page taking too long to load",
        )

    def wait_until_element_is_present(self, locator, timeout=DEFAULT):
        element = self.get_element(locator)
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(element)
        )

    def wait_for_seconds(self, seconds):
        time.sleep(seconds)

    def wait_until_element_is_clickable(self, locator, timeout=DEFAULT):
        """
        Wait till the element to be clickable
        """
        element = self.get_element(locator)
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(element)
        )

    def wait_until_element_is_visible(
        self, locator: Union[WebElement, str], timeout=DEFAULT
    ):
        """
        Wait till the element to be invisible
        """
        return self.get_element(locator, timeout)

    def wait_until_element_is_not_visible(
        self, locator: Union[WebElement, str], timeout=DEFAULT
    ) -> WebElement:
        """
        Wait till the element to be invisible
        """
        element = self.get_element(locator)
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(element)
        )

    def wait_until_page_contains_text(
        self, text: str, timeout: int = DEFAULT, error=None
    ):
        """Waits until ``text`` appears on the current page.
        Fails if ``timeout`` expires before the text appears.
        ``error`` can be used to override the default error message.
        """
        self._wait_until(
            lambda: self.is_text_present(text),
            f"Text '{text}' did not appear in <TIMEOUT>.",
            timeout,
            error,
        )

    def wait_until_page_does_not_contain_text(
        self, text: str, timeout: int = DEFAULT, error=None
    ):
        """Waits until ``text`` disappears from the current page.
        Fails if ``timeout`` expires before the text disappears.
        ``error`` can be used to override the default error message.
        """

        self._wait_until(
            lambda: not self.is_text_present(text),
            f"Text '{text}' did not disappear in <TIMEOUT>.",
            timeout,
            error,
        )

    def wait_until_page_contains_element(
        self,
        locator: Union[WebElement, None, str],
        timeout: int = DEFAULT,
        error=None,
    ):
        """Waits until the element ``locator`` appears on the current page.
        Fails if ``timeout`` expires before the element appears.
        ``error`` can be used to override the default error message.
        """
        return self._wait_until(
            lambda: self.get_element(locator) is not None,
            f"Element '{locator}' did not appear in <TIMEOUT>.",
            timeout,
            error,
        )

    def wait_until_page_does_not_contain_element(
        self,
        locator: Union[WebElement, None, str],
        timeout: int = DEFAULT,
        error=None,
    ):
        """Waits until the element ``locator`` appears on the current page.
        Fails if ``timeout`` expires before the element appears.
        ``error`` can be used to override the default error message.
        """
        return self._wait_until(
            lambda: self.get_element(locator) is None,
            f"Element '{locator}' did not appear in <TIMEOUT>.",
            timeout,
            error,
        )

    def wait_until_element_contains_text(
        self,
        locator: Union[WebElement, None, str],
        text: str,
        timeout: int = DEFAULT,
        error=None,
    ):
        """Waits until the element ``locator`` appears on the current page.
        Fails if ``timeout`` expires before the element appears.
        ``error`` can be used to override the default error message.
        """
        element = self.get_element(locator)
        self._wait_until(
            lambda: text in self.get_text(element),
            f"Element '{locator}' did not get text '{text}' in <TIMEOUT>.",
            timeout,
            error,
        )

    def wait_until_element_does_not_contain_text(
        self,
        locator: Union[WebElement, None, str],
        text: str,
        timeout: int = DEFAULT,
        error=None,
    ):
        """Waits until the element ``locator`` appears on the current page.
        Fails if ``timeout`` expires before the element appears.
        ``error`` can be used to override the default error message.
        """
        element = self.get_element(locator)
        self._wait_until(
            lambda: text not in self.get_text(element),
            f"Element '{locator}' did not get text '{text}' in <TIMEOUT>.",
            timeout,
            error,
        )

    def _wait_until(self, condition, error, timeout=DEFAULT, custom_error=None):
        if custom_error is None:
            error = error.replace("<TIMEOUT>", f"{timeout} Seconds")
        else:
            error = custom_error
        self._wait_until_worker(condition, timeout, error)

    def _wait_until_worker(self, condition, timeout, error):
        max_time = time.time() + timeout
        not_found = None
        while time.time() < max_time:
            try:
                if condition():
                    return
            except ElementNotFoundException as err:
                not_found = f"{error}{str(err)}"
            except StaleElementReferenceException as err:
                logger.info("Suppressing StaleElementReferenceException from Selenium.")
                not_found = f"{error}{str(err)}"
            time.sleep(0.2)
        raise AssertionError(not_found or error)

    # endregion

    # region helper methods

    def is_text_present(self, text: str) -> bool:
        xpath = f"//*[contains(., '{text}')]"
        self.get_element(xpath)
        return True

    def execute_script(self, locator: Union[WebElement, str], script, timeout=DEFAULT):
        """
        Execute JavaScript using web driver on selected web element
        :param: Javascript to be execute
        :return: None / depends on Script
        """
        element = self.get_element(locator, timeout)
        return self.driver.execute_script(script, element)

    def handle_exception(self, thrown_exception, message):
        logger.error(message)
        raise thrown_exception(message)

    # endregion

    def get_element_attribute(
        self, locator: Union[WebElement, str], attribute: str
    ) -> str:
        """Returns the value of ``attribute`` from the element ``locator``."""
        return self.get_element(locator).get_attribute(attribute)

    def element_attribute_value_should_be(
        self,
        locator: Union[WebElement, str],
        attribute: str,
        expected: Union[None, str],
        message: Optional[str] = None,
    ):
        """Verifies element identified by ``locator`` contains expected attribute value."""
        current_expected = self.get_element(locator).get_attribute(attribute)
        if current_expected != expected:
            if message is None:
                message = (
                    f"Element '{locator}' attribute should have value '{expected}' "
                    f"({type_converter(expected)}) but its value was '{current_expected}' "
                    f"({type_converter(current_expected)})."
                )
            raise AssertionError(message)
        logger.info(
            f"Element '{locator}' attribute '{attribute}' contains value '{expected}'."
        )

    def get_horizontal_position(self, locator: Union[WebElement, str]) -> int:
        """Returns the horizontal position of the element identified by ``locator``.


        The position is returned in pixels off the left side of the page,
        as an integer.

        """
        return self.get_element(locator).location["x"]

    def get_element_size(self, locator: Union[WebElement, str]) -> Tuple[int, int]:
        """Returns width and height of the element identified by ``locator``.

        Both width and height are returned as integers.

        """
        element = self.get_element(locator)
        return element.size["width"], element.size["height"]

    def get_value(self, locator: Union[WebElement, str]) -> str:
        """Returns the value attribute of the element identified by ``locator``."""
        return self.get_element_attribute(locator, "value")

    def get_vertical_position(self, locator: Union[WebElement, str]) -> int:
        """Returns the vertical position of the element identified by ``locator``.

        The position is returned in pixels off the top of the page,
        as an integer.
        """
        return self.get_element(locator).location["y"]

    def set_focus_to_element(self, locator: Union[WebElement, str]):
        """Sets the focus to the element identified by ``locator``."""
        element = self.get_element(locator)
        self.driver.execute_script("arguments[0].focus();", element)

    def scroll_element_into_view(self, locator: Union[WebElement, str]):
        """Scrolls the element identified by ``locator`` into view."""
        element = self.get_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def get_all_links(self) -> List[str]:
        """Returns a list containing ids of all links found in current page.

        If a link has no id, an empty string will be in the list instead.
        """
        links = self.get_elements("tag=a")
        return [link.get_attribute("id") for link in links]

    def get_element_count(self, locator: Union[WebElement, str]) -> int:
        """Returns the number of elements matching ``locator``.

        If you wish to assert the number of matching elements, use
        `Page Should Contain Element` with ``limit`` argument. Keyword will
        always return an integer.

        """
        return len(self.get_elements(locator))
