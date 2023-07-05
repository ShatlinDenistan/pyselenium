import logging as logger
from utils.common import verify_text_contains

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from automation.selenium_base import SeleniumBase
from automation.wait_times import DEFAULT
from typing import List, Optional, Tuple, Union


class Checks(SeleniumBase):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.info("Checks  initialized")

    def is_checked(self, locator: Union[WebElement, str]) -> bool:
        """
        Check if Radio button / CheckBox is selected
        :param: WebElement or locator string
        :return: Boolean
        """
        element = self.get_element(locator)
        return element.is_selected()

    def element_exists(self, locator, timeout=DEFAULT) -> bool:
        """
        checking if element exists")
        :param: locator: WebElement or locator string
        :return: Boolean
        """
        try:
            self.get_element(locator, timeout)
            return True
        except Exception:
            return False

    def child_element_exists(
        self, parent_element: WebElement, child_locator: Union[WebElement, str]
    ) -> bool:
        """
        checking if the given parent element contains child element")
        :param: parent_element: WebElement
        :param: parent_element: WebElement
        :return: Boolean
        """
        try:
            element = self.get_element(child_locator)
            if isinstance(element, WebElement):
                self.driver.find_element(element)
            else:
                parent_element.find_element(element[0], element[1])
        except Exception:
            return False
        return True

    def child_element_exists_by_locators(self, parent_locator, child_locator):
        try:
            parent_element = self.get_element(parent_locator)
            locator_tuple = self._get_locator_tuple(child_locator)
            parent_element.find_element(locator_tuple[0], locator_tuple[1])
        except NoSuchElementException:
            return False
        return True

    def page_should_contain(self, text: str):
        """Verifies that current page contains ``text``.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional ``loglevel``
        argument. Valid log levels are ``TRACE`` (default), ``DEBUG``,
        ``INFO``, ``WARN``, and ``NONE``. If the log level is ``NONE``
        or below the current active log level the source will not be logged.
        """
        if not self._page_contains(text):
            raise AssertionError(
                f"Page should have contained text '{text}' but did not."
            )
        logger.info(f"Current page contains text '{text}'.")

    def page_should_contain_element(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        """Verifies that element ``locator`` is found on the current page.

        The ``message`` argument can be used to override the default error
        message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is ``None`` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.


        """
        if limit is None:
            return self.assert_page_contains(
                locator,
                message=message,
            )
        count = len(self.get_elements(locator))
        if count == limit:
            logger.info(f"Current page contains {count} element(s).")
        else:
            if message is None:
                message = (
                    f'Page should have contained "{limit}" element(s), '
                    f'but it did contain "{count}" element(s).'
                )
            raise AssertionError(message)

    def page_should_not_contain(self, text: str):
        """Verifies the current page does not contain ``text``."""
        if self._page_contains(text):
            raise AssertionError(f"Page should not have contained text '{text}'.")
        logger.info(f"Current page does not contain text '{text}'.")

    def page_should_not_contain_element(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies that element ``locator`` is not found on the current page."""
        self.assert_page_not_contains(
            locator,
            message=message,
        )

    def element_should_be_disabled(self, locator: Union[WebElement, str]):
        """Verifies that element identified by ``locator`` is disabled.

        This keyword considers also elements that are read-only to be
        disabled.


        """
        if self.is_element_enabled(locator):
            raise AssertionError(f"Element '{locator}' is enabled.")

    def element_should_be_enabled(self, locator: Union[WebElement, str]):
        """Verifies that element identified by ``locator`` is enabled.

        This keyword considers also elements that are read-only to be
        disabled.


        """
        if not self.is_element_enabled(locator):
            raise AssertionError(f"Element '{locator}' is disabled.")

    def element_should_be_focused(self, locator: Union[WebElement, str]):
        """Verifies that element identified by ``locator`` is focused."""
        element = self.get_element(locator)
        focused = self.driver.switch_to.active_element
        # Selenium 3.6.0 with Firefox return dict which contains the selenium WebElement
        if isinstance(focused, dict):
            focused = focused["value"]
        if element != focused:
            raise AssertionError(f"Element '{locator}' does not have focus.")

    def element_should_be_visible(
        self, locator: Union[WebElement, str], message: Optional[str] = None
    ):
        """Verifies that the element identified by ``locator`` is visible.

        Herein, visible means that the element is logically visible, not
        optically visible in the current browser viewport. For example,
        an element that carries ``display:none`` is not logically visible,
        so using this keyword on that element would fail.

        The ``message`` argument can be used to override the default error
        message.
        """
        if not self.get_element(locator).is_displayed():
            if message is None:
                message = f"The element '{locator}' should be visible, but it is not."
            raise AssertionError(message)
        logger.info(f"Element '{locator}' is displayed.")

    def element_should_not_be_visible(
        self, locator: Union[WebElement, str], message: Optional[str] = None
    ):
        """Verifies that the element identified by ``locator`` is NOT visible.

        Passes if the element does not exists.
        """
        element = self.get_element(locator, required=False)
        if element is None:
            logger.info(f"Element '{locator}' did not exist.")
        elif not element.is_displayed():
            logger.info(f"Element '{locator}' exists but is not displayed.")
        else:
            if message is None:
                message = f"The element '{locator}' should not be visible, but it is."
            raise AssertionError(message)

    def element_text_should_be(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: Optional[str] = None,
        ignore_case: bool = False,
    ):
        """Verifies that element ``locator`` contains exact the text ``expected``.

        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.

        """
        logger.info(f"Verifying element '{locator}' contains exact text '{expected}'.")
        text = before_text = self.get_element(locator).text
        if ignore_case:
            text = text.lower()
            expected = expected.lower()
        if text != expected:
            if message is None:
                message = (
                    f"The text of element '{locator}' should have been '{expected}' "
                    f"but it was '{before_text}'."
                )
            raise AssertionError(message)

    def element_text_should_not_be(
        self,
        locator: Union[WebElement, str],
        not_expected: str,
        message: Optional[str] = None,
        ignore_case: bool = False,
    ):
        """Verifies that element ``locator`` does not contain exact the text ``not_expected``.



        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.


        """
        logger.info(
            f"Verifying element '{locator}' does not contain exact text '{not_expected}'."
        )
        text = self.get_element(locator).text
        before_not_expected = not_expected
        if ignore_case:
            text = text.lower()
            not_expected = not_expected.lower()
        if text == not_expected:
            if message is None:
                message = f"The text of element '{locator}' was not supposed to be '{before_not_expected}'."
            raise AssertionError(message)

    def assert_page_contains(
        self,
        locator: str,
        message: Optional[str] = None,
    ):
        if not self.get_element(locator, required=False):
            if message is None:
                message = f"Page should have contained  '{locator}' but did not."
            raise AssertionError(message)
        logger.info(f"Current page contains  '{locator}'.")

    def assert_page_not_contains(
        self,
        locator: str,
        message: Optional[str] = None,
    ):
        if self.get_element(locator, required=False):
            if message is None:
                message = f"Page should not have contained '{locator}'."
            raise AssertionError(message)
        logger.info(f"Current page does not contain  '{locator}'.")

    def _page_contains(self, text):
        self.driver.switch_to.default_content()

        if self.is_text_present(text):
            return True

        subframes = self.get_elements("xpath://frame|//iframe")
        for frame in subframes:
            self.driver.switch_to.frame(frame)
            found_text = self.is_text_present(text)
            self.driver.switch_to.default_content()
            if found_text:
                return True
        return False

    def location_should_be(self, url: str, message: Optional[str] = None):
        """Verifies that the current URL is exactly ``url``.

        The ``url`` argument contains the exact url that should exist in browser.

        The ``message`` argument can be used to override the default error
        message.


        """
        actual = self.get_location()
        if actual != url:
            if message is None:
                message = f"Location should have been '{url}' but was '{actual}'."
            raise AssertionError(message)
        logger.info(f"Current location is '{url}'.")

    def location_should_contain(self, expected: str, message: Optional[str] = None):
        """Verifies that the current URL contains ``expected``.

        The ``expected`` argument contains the expected value in url.

        The ``message`` argument can be used to override the default error
        message.

        """
        actual = self.get_location()
        if expected not in actual:
            if message is None:
                message = (
                    f"Location should have contained '{expected}' but "
                    f"it was '{actual}'."
                )
            raise AssertionError(message)
        logger.info(f"Current location contains '{expected}'.")

    def title_should_be(self, title: str, message: Optional[str] = None):
        """Verifies that the current page title equals ``title``.

        The ``message`` argument can be used to override the default error
        message.

        """
        actual = self.get_title()
        if actual != title:
            if message is None:
                message = f"Title should have been '{title}' but was '{actual}'."
            raise AssertionError(message)

    def is_element_enabled(self, locator: str) -> bool:
        element = self.get_element(locator)
        return element.is_enabled() and element.get_attribute("readonly") is None

    def element_should_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: Optional[str] = None,
        ignore_case: bool = False,
    ):
        """Verifies that element ``locator`` contains text ``expected``.



        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.

        Use `Element Text Should Be` if you want to match the exact text,
        not a substring.
        """
        actual = actual_before = self.get_element(locator).text
        expected_before = expected
        if ignore_case:
            actual = actual.lower()
            expected = expected.lower()
        if expected not in actual:
            if message is None:
                message = (
                    f"Element '{locator}' should have contained text '{expected_before}' but "
                    f"its text was '{actual_before}'."
                )
            raise AssertionError(message)
        logger.info(f"Element '{locator}' contains text '{expected_before}'.")

    def element_should_not_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: str = "",
        ignore_case: bool = False,
    ):
        """Verifies that element ``locator`` does not contain text ``expected``.



        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.

        """
        actual = self.get_element(locator).text
        expected_before = expected
        if ignore_case:
            actual = actual.lower()
            expected = expected.lower()
        if expected in actual:
            if message is None:
                message = (
                    f"Element '{locator}' should not contain text '{expected_before}' but "
                    "it did."
                )
            raise AssertionError(message)
        logger.info(f"Element '{locator}' does not contain text '{expected_before}'.")

    def verify_page_title(self, title_to_verity):
        try:
            actual_title = self.getTitle()
            return verify_text_contains(actual_title, title_to_verity)
        except Exception:
            self.log.error("Failed to get page title")
            return False

    def page_should_contain_link(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies link identified by ``locator`` is found from current page.

         When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.


        """
        self.assert_page_contains(locator, message)

    def page_should_not_contain_link(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies link identified by ``locator`` is not found from current page.

         When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.


        """
        self.assert_page_not_contains(locator, message)

    def page_should_contain_button(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies button ``locator`` is found from current page.



         When using the default locator strategy, buttons are
        searched using ``id``, ``name``, and ``value``.
        """
        try:
            self.assert_page_contains(
                locator,
                message,
            )
        except AssertionError:
            self.assert_page_contains(
                locator,
                message,
            )

    def page_should_not_contain_button(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies button ``locator`` is not found from current page.
        When using the default locator strategy, buttons are
        searched using ``id``, ``name``, and ``value``.
        """
        self.assert_page_not_contains(locator, message)

    def checkbox_should_be_selected(self, locator: Union[WebElement, str]):
        """Verifies checkbox ``locator`` is selected/checked."""
        logger.info(f"Verifying checkbox '{locator}' is selected.")
        element = self._get_checkbox(locator)
        if not element.is_selected():
            raise AssertionError(
                f"Checkbox '{locator}' should have been selected but was not."
            )

    def checkbox_should_not_be_selected(self, locator: Union[WebElement, str]):
        """Verifies checkbox ``locator`` is not selected/checked."""
        logger.info(f"Verifying checkbox '{locator}' is not selected.")
        element = self._get_checkbox(locator)
        if element.is_selected():
            raise AssertionError(f"Checkbox '{locator}' should not have been selected.")

    def page_should_contain_checkbox(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies checkbox ``locator`` is found from the current page."""
        self.assert_page_contains(locator, message)

    def page_should_not_contain_checkbox(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies checkbox ``locator`` is not found from the current page."""
        self.assert_page_not_contains(locator, message)

    def page_should_contain_radio_button(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies radio button ``locator`` is found from current page.

        When using the default locator strategy, radio buttons are
        searched using ``id``, ``name`` and ``value``.
        """
        self.assert_page_contains(locator, message)

    def page_should_not_contain_radio_button(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies radio button ``locator`` is not found from current page.


         When using the default locator strategy, radio buttons are
        searched using ``id``, ``name`` and ``value``.
        """
        self.assert_page_not_contains(locator, message)

    def radio_button_should_be_set_to(self, group_name: str, value: str):
        """Verifies radio button group ``group_name`` is set to ``value``.

        ``group_name`` is the ``name`` of the radio button group.
        """
        logger.info(f"Verifying radio button '{group_name}' has selection '{value}'.")
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is None or actual_value != value:
            raise AssertionError(
                f"Selection of radio button '{group_name}' should have "
                f"been '{value}' but was '{actual_value}'."
            )

    def radio_button_should_not_be_selected(self, group_name: str):
        """Verifies radio button group ``group_name`` has no selection.

        ``group_name`` is the ``name`` of the radio button group.
        """
        logger.info(f"Verifying radio button '{group_name}' has no selection.")
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is not None:
            raise AssertionError(
                f"Radio button group '{group_name}' should not have "
                f"had selection, but '{actual_value}' was selected."
            )

    def page_should_contain_textfield(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies text field ``locator`` is found from current page."""
        self.assert_page_contains(locator, message)

    def page_should_not_contain_textfield(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies text field ``locator`` is not found from current page."""
        self.assert_page_not_contains(locator, message)

    def textfield_should_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ):
        """Verifies text field ``locator`` contains text ``expected``.

        ``message`` can be used to override the default error message.


        """
        actual = self._get_value(locator)
        if expected not in actual:
            if message is None:
                message = (
                    f"Text field '{locator}' should have contained text "
                    f"'{expected}' but it contained '{actual}'."
                )
            raise AssertionError(message)
        logger.info(f"Text field '{locator}' contains text '{expected}'.")

    def textfield_value_should_be(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ):
        """Verifies text field ``locator`` has exactly text ``expected``.

        ``message`` can be used to override default error message.

        """
        actual = self._get_value(locator)
        if actual != expected:
            if message is None:
                message = (
                    f"Value of text field '{locator}' should have been "
                    f"'{expected}' but was '{actual}'."
                )
            raise AssertionError(message)
        logger.info(f"Content of text field '{locator}' is '{expected}'.")

    def textarea_should_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ):
        """Verifies text area ``locator`` contains text ``expected``.

        ``message`` can be used to override default error message.
        """
        actual = self._get_value(locator)
        if expected not in actual:
            if message is None:
                message = (
                    f"Text area '{locator}' should have contained text "
                    f"'{expected}' but it had '{actual}'."
                )
            raise AssertionError(message)
        logger.info(f"Text area '{locator}' contains text '{expected}'.")

    def textarea_value_should_be(
        self,
        locator: Union[WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ):
        """Verifies text area ``locator`` has exactly text ``expected``.

        ``message`` can be used to override default error message.
        """
        actual = self._get_value(locator)
        if expected != actual:
            if message is None:
                message = (
                    f"Text area '{locator}' should have had text "
                    f"'{expected}' but it had '{actual}'."
                )
            raise AssertionError(message)
        logger.info(f"Content of text area '{locator}' is '{expected}'.")
