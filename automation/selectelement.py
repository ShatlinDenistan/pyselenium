from selenium.webdriver.support.ui import Select
from automation.selenium_base import SeleniumBase
from typing import List, Optional, Union
from selenium.webdriver.remote.webelement import WebElement

from utils.common import plural_or_not
import logging as logger


class SelectElement(SeleniumBase):
    def get_select_items(
        self, locator: Union[WebElement, str], values: bool = False
    ) -> List[str]:
        """Returns all labels or values of selection list ``locator``."""
        options = self._get_options(locator)
        return self._get_values(options) if values else self._get_labels(options)

    def get_selected_list_label(self, locator: Union[WebElement, str]) -> str:
        """Returns the label of selected option from selection list ``locator``."""
        select = self._get_select_list(locator)
        return select.first_selected_option.text

    def get_selected_list_labels(self, locator: Union[WebElement, str]) -> List[str]:
        """Returns labels of selected options from selection list ``locator``."""
        options = self._get_selected_options(locator)
        return self._get_labels(options)

    def get_selected_list_value(self, locator: Union[WebElement, str]) -> str:
        """Returns the value of selected option from selection list ``locator``."""
        select = self._get_select_list(locator)
        return select.first_selected_option.get_attribute("value")

    def get_selected_list_values(self, locator: Union[WebElement, str]) -> List[str]:
        """Returns values of selected options from selection list ``locator``."""
        options = self._get_selected_options(locator)
        return self._get_values(options)

    def list_selection_should_be(self, locator: Union[WebElement, str], *expected: str):
        """Verifies selection list ``locator`` has ``expected`` options selected."""

        self.page_should_contain_list(locator)
        options = self._get_selected_options(locator)
        labels = self._get_labels(options)
        values = self._get_values(options)
        if sorted(expected) not in [sorted(labels), sorted(values)]:
            raise AssertionError(
                f"List '{locator}' should have had selection [ {' | '.join(expected)} ] "
                f"but selection was [ {self._format_selection(labels, values)} ]."
            )

    def list_should_have_no_selections(self, locator: Union[WebElement, str]):
        """Verifies selection list ``locator`` has no options selected."""
        logger.info(f"Verifying list '{locator}' has no selections.")
        if options := self._get_selected_options(locator):
            selection = self._format_selection(
                self._get_labels(options), self._get_values(options)
            )
            raise AssertionError(
                f"List '{locator}' should have had no selection "
                f"but selection was [ {selection} ]."
            )

    def get_select_list_count(self, locator):
        """
        Count of Item from Dropdown
        :param: None
        :return: count
        """
        select = self._get_select_list(locator)
        return len(select.options)

    def list_should_contain_label(self, locator, text):
        """
        Verify text to be present in  Dropdown
        :param: item to be verify
        :return: True / False
        """
        select = self._get_select_list(locator)
        return any(text == item.text for item in select.options)

    def list_should_contain_value(self, locator, text):
        """
        Verify text to be present in  Dropdown
        :param: item to be verify
        :return: True / False
        """
        select = self._get_select_list(locator)
        return any(text == item.get_attribute("value") for item in select.options)

    def page_should_contain_list(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies selection list ``locator`` is found from current page."""
        self.assert_page_contains(locator, message)

    def page_should_not_contain_list(
        self,
        locator: Union[WebElement, str],
        message: Optional[str] = None,
    ):
        """Verifies selection list ``locator`` is not found from current page."""
        self.assert_page_not_contains(locator, message)

    def select_all_from_list(self, locator: Union[WebElement, str]):
        """Selects all options from multi-selection list ``locator``."""
        logger.info(f"Selecting all options from list '{locator}'.")
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError(
                "'Select All From List' works only with multi-selection lists."
            )
        for index in range(len(select.options)):
            select.select_by_index(index)

    def select_from_list_by_index(self, locator: Union[WebElement, str], *indexes: str):
        """Selects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.
        """
        if not indexes:
            raise ValueError("No indexes given.")
        plural = "" if len(indexes) == 1 else "es"
        logger.info(
            f"Selecting options from selection list '{locator}' "
            f"by index{plural} {', '.join(indexes)}."
        )
        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    def select_from_list_by_value(self, locator: Union[WebElement, str], *values: str):
        """Selects options from selection list ``locator`` by ``values``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.
        """
        if not values:
            raise ValueError("No values given.")
        logger.info(
            f"Selecting options from selection list '{locator}' by "
            f"value{plural_or_not(values)} {', '.join(values)}."
        )
        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    def select_from_list_by_label(self, locator: Union[WebElement, str], *labels: str):
        """Selects options from selection list ``locator`` by ``labels``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        """
        if not labels:
            raise ValueError("No labels given.")
        logger.info(
            f"Selecting options from selection list '{locator}' "
            f"by label{plural_or_not(labels)} {', '.join(labels)}."
        )
        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    def unselect_all_from_list(self, locator: Union[WebElement, str]):
        """Unselects all options from multi-selection list ``locator``."""
        logger.info(f"Unselecting all options from list '{locator}'.")
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self._raise_runtime_error()

        select.deselect_all()

    def unselect_from_list_by_value(
        self, locator: Union[WebElement, str], *values: str
    ):
        """Unselects options from selection list ``locator`` by ``values``.

        This keyword works only with multi-selection lists.
        """
        if not values:
            raise ValueError("No values given.")
        logger.info(
            f"Un-selecting options from selection list '{locator}' by "
            f"value{plural_or_not(values)} {', '.join(values)}."
        )
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self._raise_runtime_error()
        for value in values:
            select.deselect_by_value(value)

    def unselect_from_list_by_label(
        self, locator: Union[WebElement, str], *labels: str
    ):
        """Unselects options from selection list ``locator`` by ``labels``.

        This keyword works only with multi-selection lists.
        """
        if not labels:
            raise ValueError("No labels given.")
        logger.info(
            f"Un-selecting options from selection list '{locator}' by "
            f"label{plural_or_not(labels)} {', '.join(labels)}."
        )
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self._raise_runtime_error()

        for label in labels:
            select.deselect_by_visible_text(label)

    def unselect_from_list_by_index(
        self, locator: Union[WebElement, str], *indexes: str
    ):
        """Unselects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0. This keyword works only with
        multi-selection lists.
        """
        if not indexes:
            raise ValueError("No indexes given.")
        plurar = "" if len(indexes) == 1 else "es"
        logger.info(
            f"Un-selecting options from selection list '{locator}' by index{plurar} "
            f"{', '.join(indexes)}."
        )
        select = self._get_select_list(locator)
        if not select.is_multiple:
            self._raise_runtime_error()
        for index in indexes:
            select.deselect_by_index(int(index))

    def _get_select_list(self, locator):
        element = self.get_element(self, locator)
        return Select(element)

    def _get_options(self, locator: Union[WebElement, str]):
        return self._get_select_list(locator).options

    def _get_labels(self, options):
        return [opt.text for opt in options]

    def _get_values(self, options):
        return [opt.get_attribute("value") for opt in options]

    def _get_selected_options(self, locator: Union[WebElement, str]):
        return self._get_select_list(locator).all_selected_options

    def _format_selection(self, labels, values):
        return " | ".join(f"{label} ({value})" for label, value in zip(labels, values))

    def _raise_runtime_error(self) -> None:
        raise RuntimeError(
            "Un-selecting options works only with multi-selection lists."
        )
