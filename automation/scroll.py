import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from automation.selenium_base import SeleniumBase
from selenium.webdriver.remote.webdriver import WebDriver


class Scroll(SeleniumBase):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def scroll_down(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_DOWN).perform()

    def scroll_down_til_the_end(self):
        scroll_height_script = "return document.body.scrollHeight"
        scroll_top_script = "window.scrollTo(0, document.body.scrollHeight)"
        last_height = self.driver.execute_script(scroll_height_script)
        while True:
            self.driver.\
                execute_script(scroll_top_script)
            time.sleep(0.5)
            new_height = self.driver.execute_script(scroll_height_script)
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_up(self):
        action = ActionChains(self.driver)
        action.send_keys(Keys.PAGE_UP).perform()

    def scroll_page_down(self):
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def scroll_page_up(self):
        self.driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")

    def scroll_into_view(self, locator):
        element = self.get_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(false);", element)
