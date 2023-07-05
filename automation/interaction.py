import logging as logger
from typing import Union
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from utils.common import plural_or_not
from automation.wait_times import DEFAULT
from automation.selenium_base import SeleniumBase
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List
import os
from automation.error import ElementNotFoundException


class Interaction(SeleniumBase):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        logger.info("Interaction  initialized")

    def get_attribute(self, locator: Union[WebElement, str], attribute_name):
        """
        get webElement attribute
        :param: name of Attribute
        :return: webElement attribute value
        """
        element = self.get_element(locator)
        return element.get_attribute(attribute_name)

    def set_attribute(self, locator: Union[WebElement, str], attribute_name, value):
        """
        set webElement attribute
        :param: name of Attribute
        :return: webElement attribute value
        """
        element = self.get_element(locator)

        return self.driver.execute_script(
            f"arguments[0].setAttribute({attribute_name},{value})", element
        )

    def highlight_web_element(self, element):
        """
        To highlight webElement
        :param: WebElement
        :return: None
        """
        self.driver.execute_script(
            "arguments[0].style.border='2px ridge #33ffff'", element
        )

    def click_element(self, locator: Union[WebElement, str]) -> WebElement:
        # logger.info("clicking %s", locator)
        """
        Perform  click on webElement
        :param: None
        :return: webElement
        """
        element = self.wait_until_element_is_clickable(locator)
        element.click()
        return element

    def click_element_at_coordinates(
        self, locator: Union[WebElement, str], xoffset: int, yoffset: int
    ):
        """Click the element ``locator`` at ``xoffset/yoffset``.
        The Cursor is moved and the center of the element and x/y coordinates are
        calculated from that point.
        """
        logger.info(
            f"Clicking element '{locator}' at coordinates x={xoffset}, y={yoffset}."
        )
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.move_by_offset(xoffset, yoffset)
        action.click()
        action.perform()

    def double_click_element(self, locator: Union[WebElement, str]):
        """Double clicks the element identified by ``locator``."""
        logger.info(f"Double clicking element '{locator}'.")
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.double_click(element).perform()

    def drag_and_drop(
        self, locator: Union[WebElement, str], target: Union[WebElement, str]
    ):
        """Drags the element identified by ``locator`` into the ``target`` element.

        The ``locator`` argument is the locator of the dragged element
        and the ``target`` is the locator of the target.
        """
        element = self.get_element(locator)
        target = self.get_element(target)
        action = ActionChains(self.driver)
        action.drag_and_drop(element, target).perform()

    def drag_and_drop_by_offset(
        self, locator: Union[WebElement, str], xoffset: int, yoffset: int
    ):
        """Drags the element identified with ``locator`` by ``xoffset/yoffset``.
        The element will be moved by ``xoffset`` and ``yoffset``, each of which
        is a negative or positive number specifying the offset.
        """
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, xoffset, yoffset)
        action.perform()

    def mouse_down(self, locator: Union[WebElement, str]):
        """Simulates pressing the left mouse button on the element ``locator``.

        The element is pressed without releasing the mouse button.

        """
        logger.info(f"Simulating Mouse Down on element '{locator}'.")
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    def mouse_out(self, locator: Union[WebElement, str]):
        """Simulates moving the mouse away from the element ``locator``."""
        logger.info(f"Simulating Mouse Out on element '{locator}'.")
        element = self.get_element(locator)
        size = element.size
        offsetx = (size["width"] / 2) + 1
        offsety = (size["height"] / 2) + 1
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.move_by_offset(offsetx, offsety)
        action.perform()

    def mouse_over(self, locator: Union[WebElement, str]):
        """Simulates hovering the mouse over the element ``locator``."""
        logger.info(f"Simulating Mouse Over on element '{locator}'.")
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    def mouse_up(self, locator: Union[WebElement, str]):
        """Simulates releasing the left mouse button on the element ``locator``."""
        logger.info(f"Simulating Mouse Up on element '{locator}'.")
        element = self.get_element(locator)
        ActionChains(self.driver).release(element).perform()

    def open_context_menu(self, locator: Union[WebElement, str]):
        """Opens the context menu on the element identified by ``locator``."""
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    def clear_element_text(self, locator: Union[WebElement, str]):
        """Clears the value of the text-input-element identified by ``locator``."""
        self.get_element(locator).clear()

    def click_and_hold(self, locator: Union[WebElement, str]) -> WebElement:
        """
        This method will replace the moveToElement(onElement).clickAndHold()
        Added support for Selenium 4
        :param: None
        :return: webElement
        """
        element = self.wait_until_element_is_clickable(locator)
        ActionChains(self.driver).click_and_hold(on_element=element)
        return element

    def _click_with_action_chain(self, locator: Union[WebElement, str]):
        logger.info(f"Clicking '{locator}' using an action chain.")
        action = ActionChains(self.driver)
        element = self.get_element(locator)
        action.move_to_element(element)
        action.click()
        action.perform()

    def release(self, locator: Union[WebElement, str]) -> WebElement:
        """
        Releasing a held mouse button on an element.
        Added support for Selenium 4
        :param: None
        :return: webElement
        """
        element = self.get_element(locator)
        ActionChains(self.driver).release(on_element=element)
        return element

    def set_text(self, locator: Union[WebElement, str], value) -> WebElement:
        """
        type text in input box
        :param: Text to be Enter
        :return: webElement
        """
        element = self.wait_until_element_is_clickable(locator)
        element.send_keys(value)
        return element

    def get_value(self, locator, timeout=DEFAULT):
        element = self.get_element(locator, timeout)
        return None if element is None else element.get_attribute("value")

    def clear_text(self, locator: Union[WebElement, str]) -> WebElement:
        """
        Clear text from EditBox
        :param: None
        :return: None
        """
        element = self.get_element(locator)
        element.clear()
        return element

    def hover(self, locator: Union[WebElement, str]) -> WebElement:
        """
        perform hover operation on webElement
        :param: None
        :return: None
        """
        # logger.info("hovering over %s", locator)

        element = self.get_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
        return element

    def press_keys(self, locator: Union[WebElement, None, str] = None, *keys: str):
        """Simulates the user pressing key(s) to an element or on the active browser."""
        parsed_keys = self._parse_keys(*keys)
        logger.info(f"Sending key(s) {keys} to {locator} element.")
        element = self.get_element(locator)
        ActionChains(self.driver).click(element).perform()
        for parsed_key in parsed_keys:
            actions = ActionChains(self.driver)
            for key in parsed_key:
                if key.special:
                    self._press_keys_special_keys(actions, element, parsed_key, key)
                else:
                    self._press_keys_normal_keys(actions, key)
            self._special_key_up(actions, parsed_key)
            actions.perform()

    def _press_keys_normal_keys(self, actions, key):
        logger.info(f"Sending key{plural_or_not(key.converted)} {key.converted}")
        actions.send_keys(key.converted)

    def _press_keys_special_keys(self, actions, element, parsed_key, key):
        if len(parsed_key) == 1 and element:
            logger.info(f"Pressing special key {key.original} to element.")
            actions.send_keys(key.converted)
        elif len(parsed_key) == 1:
            logger.info(f"Pressing special key {key.original} to browser.")
            actions.send_keys(key.converted)
        else:
            logger.info(f"Pressing special key {key.original} down.")
            actions.key_down(key.converted)

    def _special_key_up(self, actions, parsed_key):
        for key in parsed_key:
            if key.special:
                logger.info(f"Releasing special key {key.original}.")
                actions.key_up(key.converted)

    def submit(self, locator):
        self.get_element(locator).submit()

    def get_url(self, locator):
        return self.get_element(locator).get_attribute("href")

    def click_by_js(self, locator, timeout=DEFAULT):
        element = self.get_element(locator, timeout)
        # logger.info("clicking element using javascript")
        self.driver.execute_script("arguments[0].click()", element)

    def send_keys_by_js(self, locator: Union[WebElement, str], text, timeout=DEFAULT):
        element = self.get_element(locator, timeout)
        # logger.info("sening keys  element using javascript")
        self.driver.execute_script(f"arguments[0].value='{text}';", element)

    def change_color(self, locator: Union[WebElement, str], color, timeout=DEFAULT):
        element = self.get_element(locator, timeout)

        self.driver.execute_script(
            self, f"arguments[0].style.backgroundColor = '{color}'", element
        )

    def draw_border(self, locator: Union[WebElement, str], timeout=DEFAULT):
        element = self.get_element(locator, timeout)
        self.driver.execute_script(
            "arguments[0].style.border = '3px solid red'", element
        )

    def refresh_page_by_js(self):
        self.driver.execute_script("history.go(0)")

    def get_page_title_by_js(self):
        return self.driver.execute_script("return document.title")

    def get_page_inner_text_by_js(self):
        return self.driver.execute_script("return document.documentElement.innerText")

    def select_date(self, locator: Union[WebElement, str], date, timeout=DEFAULT):
        element = self.get_element(locator, timeout)
        self.driver.execute_script
        (f"arguments[0].setAttribute('value', '{date}')", element)

    def focus(self, locator: Union[WebElement, str], timeout=DEFAULT):
        element = self.get_element(locator, timeout)
        self.driver.execute_script("arguments[0].focus();", element)

    def focus_on_page(self):
        self.driver.execute_script("window.focus();")

    def mouse_down_on_image(self, locator: Union[WebElement, str]):
        """Simulates a mouse down event on an image identified by ``locator``.

        When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.
        """
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    def mouse_down_on_link(self, locator: Union[WebElement, str]):
        """Simulates a mouse down event on a link identified by ``locator``.

        When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.
        """
        element = self.get_element(locator)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    def submit_form(self, locator: Union[WebElement, None, str] = None):
        """Submits a form identified by ``locator``.
        If ``locator`` is not given, first form on the page is submitted.
        """
        logger.info(f"Submitting form '{locator}'.")
        if locator is None:
            locator = "tag:form"
        element = self.get_element(locator)
        element.submit()

    def select_checkbox(self, locator: Union[WebElement, str]):
        """Selects the checkbox identified by ``locator``.
        Does nothing if checkbox is already selected.
        """
        logger.info(f"Selecting checkbox '{locator}'.")
        element = self._get_checkbox(locator)
        if not element.is_selected():
            element.click()

    def unselect_checkbox(self, locator: Union[WebElement, str]):
        """Removes the selection of checkbox identified by ``locator``.
        Does nothing if the checkbox is not selected.
        """
        logger.info(f"Unselecting checkbox '{locator}'.")
        element = self._get_checkbox(locator)
        if element.is_selected():
            element.click()

    def select_radio_button(self, group_name: str, value: str):
        """Sets the radio button group ``group_name`` to ``value``.
        The radio button to be selected is located by two arguments:
        - ``group_name`` is the name of the radio button group.
        - ``value`` is the ``id`` or ``value`` attribute of the actual
        radio button.
        """
        logger.info(f"Selecting '{value}' from radio button '{group_name}'.")
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            element.click()

    def choose_file(self, locator: Union[WebElement, str], file_path: str):
        """Inputs the ``file_path`` into the file input field ``locator``."""

        logger.info(f"Sending {os.path.abspath(file_path)} to browser.")
        self.get_element(locator).send_keys(file_path)

    def input_password(
        self, locator: Union[WebElement, str], password: str, clear: bool = True
    ):
        """Types the given password into the text field identified by ``locator``."""
        logger.info(f"Typing password into text field '{locator}'.")
        self._input_text_into_text_field(locator, password, clear)

    def input_text(
        self, locator: Union[WebElement, str], text: str, clear: bool = True
    ):
        """Types the given ``text`` into the text field identified by ``locator``."""
        logger.info(f"Typing text '{text}' into text field '{locator}'.")
        self._input_text_into_text_field(locator, text, clear)

    def _get_value(self, locator):
        return self.get_element(locator).get_attribute("value")

    def _get_checkbox(self, locator: Union[WebElement, str]) -> WebElement:
        return self.get_element(locator)

    def _get_radio_buttons(self, group_name):
        xpath = f"xpath://input[@type='radio' and @name='{group_name}']"
        if elements := self.get_elements(xpath):
            return elements
        else:
            raise ElementNotFoundException(
                f"No radio button with name '{group_name}' found."
            )

    def _get_radio_button_with_value(self, group_name, value) -> WebElement:
        xpath = (
            f"xpath://input[@type='radio' and @name='{group_name}' and "
            f"(@value='{value}' or @id='{value}')]"
        )
        try:
            return self.get_element(xpath)
        except ElementNotFoundException as e:
            raise ElementNotFoundException(
                f"No radio button with name '{group_name}' "
                f"and value '{value}' found."
            ) from e

    def _get_value_from_radio_buttons(self, elements: List[WebElement]) -> WebElement:
        return next(
            (
                element.get_attribute("value")
                for element in elements
                if element.is_selected()
            ),
            None,
        )

    def _input_text_into_text_field(self, locator, text, clear=True):
        element = self.get_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)
