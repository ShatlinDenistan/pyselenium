from typing import List
from automation.page_base import PageBase
from pos.home_po import HomePO
import logging as logger
import time
from config.config import BASE_URL
from datetime import datetime
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from automation.error import (
    ElementNotVisibleException,
)
import requests
from lxml import html


class CodeGenPage(PageBase):
    def generate_code(self):
        try:
            response = requests.get(
                "https://en.wikipedia.org/wiki/List_of_countries_by_population_in_2010"
            )
            tree = html.fromstring(response.text)
            countries = tree.xpath('//span[@class="flagicon"]')
            for e in tree.iter():
                print(tree.xpath(e))
            for country in countries:
                print(country.xpath("./following-sibling::a/text()")[0])
        except Exception as e:
            logger.exception(str(e))
