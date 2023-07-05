"""Test init and tear down methods"""

from dataclasses import dataclass
import logging as logger
from typing import Optional
from lxml import html
from lxml.html import HtmlElement
from utils.common import generate_random_string


@dataclass
class Script:
    """Class for keeping track of an item in inventory."""

    element_count: int
    xpath: str
    variable_name: Optional[str] = ""
    element: Optional[HtmlElement] = None
    action: Optional[str] = ""
    sequence_no: Optional[int] = 0

    def __getitem__(self, xpath=None):
        return self.xpath


class Scripter:
    incl = ["input", "button", "select", "a", "table", "span", "div"]
    all_scripts: list[Script] = []
    unique_paths: set[str] = set()
    sequence_no: int = 0
    max_variable_length: int = 20

    def __init__(self, htmlstring):
        self.html_string = htmlstring

    def generate_script(self):
        tree = html.fromstring(self.html_string)
        for element in tree.iter():
            try:
                if not self.skip_this_element(element):
                    self.construct_xpath(tree, element)
            except Exception as e:
                logger.info(
                    f"0|exception for element {element.tag} with text {element.text}|error"
                )
        for script in self.all_scripts:
            if script.xpath not in self.unique_paths:
                self.unique_paths.add(script.xpath)
                logger.info(
                    f'{script.sequence_no}|{script.element_count}|{script.variable_name} = "{script.xpath}"|{script.action}'
                )

    def skip_this_element(self, element):
        if not isinstance(element.tag, str):
            return True
        if "type" in element.attrib.keys() and element.attrib["type"] == "hidden":
            return False
        if element.tag not in self.incl:
            return True

    def construct_xpath(self, tree, element):
        # step 1: Get xpath based on text
        scripts = []
        text = self.clean_text(element.text)
        if text is not None and len(text.strip()) > 0:
            xpath = f"//{element.tag}[text()='{self.clean_text(element.text)}']"
            scripts.append(self.get_xpath_and_count(xpath, tree, element))

        for key, value in element.attrib.items():
            # step 2: Get xpath based on each attribute of the element
            xpath = f"//{element.tag}[@{key}='{self.clean_text(value)}']"
            scripts.append(self.get_xpath_and_count(xpath, tree, element))

        for index, (key, value) in enumerate(element.attrib.items()):
            # step 4: Append xpath based on each attribute of the element
            if index == 0:
                xpath = f"//{element.tag}[@{key}='{self.clean_text(value)}']"
            else:
                xpath = f"{xpath[:-1]} and @{key}='{self.clean_text(value)}']"
                scripts.append(self.get_xpath_and_count(xpath, tree, element))
        # step 5: Compare and remove less optimal xpaths
        filtered_scripts = self.select_relevant_xpaths(scripts)
        # step 6: decide a name
        name = self.generate_variable_name(filtered_scripts, element)
        name = self.clean_string(name)
        # step 7: Generate code for each selected xpath
        self.sequence_no += 1
        self.append_scripts_to_global_list(filtered_scripts, name)

    def get_xpath_and_count(self, xpath_string, tree, element):
        prefix = "xpath="
        try:
            element_in_path = tree.xpath(xpath_string)
            count_of_elements_found = len(element_in_path)
        except Exception:
            count_of_elements_found = -1

        return Script(
            element_count=count_of_elements_found,
            xpath=f"{prefix}{xpath_string}",
            element=element,
        )

    def clean_text(self, text):
        if text is None:
            return ""
        text = text.replace("\t", "")
        text = text.replace("\n", "")
        text = text.replace("\r", "")
        return text

    def generate_automation_action(self, script: Script, name):
        xpath = script.xpath
        if "input" in xpath:
            return f"self.input_text(PagePO.{name},'random')"
        else:
            return f"self.click_element(PagePO.{name})"

    def clean_string(self, text):
        text = text.replace(" ", "_")
        text = text.replace(".", "_")
        text = text.replace(":", "_")
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace("[", "")
        text = text.replace("]", "")
        text = text.replace("//", "_")
        text = text.replace("/", "_")
        text = text.replace("-", "_")
        text = text.replace("#", "_")
        text = text.replace("'", "_")
        text = text.replace('"', "_")
        text = text.replace("^", "_")
        text = text.replace(" %", "_")
        text = text.replace("–", "_")
        text = text.replace("%", "_")
        text = text.replace(",", "_")
        text = text.replace("&", "_")
        text = text.replace(";", "")
        text = text.replace("__", "_")
        return text

    def clean_element_name(self, element_name):
        element_name = element_name.split("'")[1]
        return self.clean_string(element_name)

    def generate_variable_name(self, scripts: list[Script], element):
        names = []
        for script in scripts:
            element_name = self.clean_element_name(script.xpath)
            names.append(element_name)
        if not names:
            return generate_random_string()
        smallest_name = min(names, key=len)
        if len(smallest_name) > self.max_variable_length:
            name_array = smallest_name.split("_")
            smallest_name = ""
            for names in name_array:
                smallest_name = f"{smallest_name}_{names}"
                if len(smallest_name) > self.max_variable_length:
                    smallest_name = smallest_name.replace("__", "_")[1:]
                    break
        for _ in range(3):
            smallest_name = smallest_name.replace("__", "_")
        if not smallest_name:
            return generate_random_string()
        if smallest_name[0] == "_":
            smallest_name = smallest_name[1:]
        return f"{element.tag}_{smallest_name}".lower()

    def append_scripts_to_global_list(self, scripts: list[Script], name):
        scripts = sorted(scripts, key=lambda a: len(a.xpath))
        for script in scripts:
            action = self.generate_automation_action(script, name)
            self.all_scripts.append(
                Script(
                    element_count=script.element_count,
                    variable_name=name,
                    xpath=script.xpath,
                    action=action,
                    sequence_no=self.sequence_no,
                )
            )

    def pick_winner(self, scripts: list[Script]):
        for script in scripts:
            text = self.clean_element_name(script.xpath)
            text = text.replace("_", "")
            if len(text) == 0:
                return None
            if script.xpath.count("@") == 1:
                if "@id=" in script.xpath:
                    return script
                if "@class=" in script.xpath:
                    return script
                if "@name=" in script.xpath:
                    return script
        return None

    def select_relevant_xpaths(self, scripts: list[Script]):
        return sorted(scripts, key=lambda a: len(a.xpath))
        # sort xpaths so that locators with minimum finds will be first
        # xpaths = sorted(xpaths)
        # # get the non zero number that has the lowest number of elements ( like 1 or 2)
        # # minimum_count = min(x[0] for x in xpaths if x[0] != 0)

        # # # this is required if there are zero elements, then just return all xpaths
        # # if not (min_xpaths := [x for x in xpaths if x[0] == minimum_count]):
        # #     return xpaths
        # winner = pick_winner(xpaths)
        # return [winner] if winner is not None else xpaths
        # get the xpath with the smallest string and return it
        # smallest_xpath = min_xpaths[0]
        # for item in min_xpaths:
        #     if len(item[1]) < len(smallest_xpath[1]):
        #         smallest_xpath = item
        # return [smallest_xpath] if len(smallest_xpath) > 0 else min_xpaths
