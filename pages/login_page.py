from typing import List
from automation.page_base import PageBase
from pos.login_po import LoginPO
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


class LoginPage(PageBase):
    def is_in_login_page(self):
        self.wait_until_element_is_visible(LoginPO.login_button, 40)
        return True

    def login(self, username, password):
        try:
            self.input_text(LoginPO.username_input, username)
            self.input_text(LoginPO.password_input, password)
            self.click_element(LoginPO.login_button)

        except Exception as e:
            pass
