from abc import ABC, abstractmethod
from dataclasses import dataclass
from automation.selenium_base import SeleniumBase
import logging as logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.drivers.edge import EdgeChromiumDriver


@dataclass
class BrowserStrategy(ABC):
    @abstractmethod
    def start(self):
        pass


@dataclass
class Chrome(BrowserStrategy):
    def start(self):
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--ignore-ssl-errors=yes")
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--disable-xss-auditor")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--disable-webgl")
            chrome_options.add_argument("--disable-popup-blocking")
            # driver = webdriver.Chrome(
            #     ChromeDriverManager().install(), options=chrome_options
            # )
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=chrome_options
            )

            return driver

        except Exception as e:
            logger.info(str(e))
        # return webdriver.Remote(ChromeDriverManager().install(), options=options)
        # driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
        # return driver


@dataclass
class Firefox(BrowserStrategy):
    def start(self):
        options = webdriver.FirefoxOptions()
        return webdriver.Remote(GeckoDriverManager().install(), options=options)

        # driver = webdriver.Remote(command_executor="http://localhost:4444", options=opt)
        # return driver


@dataclass
class Edge(BrowserStrategy):
    def start(self):
        # return webdriver.Remote(EdgeChromiumDriver().install())
        return webdriver.Remote(
            command_executor="http://localhost:4444/wd/hub",
            desired_capabilities={
                "browserName": "MicrosoftEdge",
                "ms:edgeOptions": {"args": ["--remote-allow-origins=*"]},
                "platformName": "mac",
            },
        )


@dataclass
class Safari(BrowserStrategy):
    def start(self):
        raise NotImplementedError


class BrowserSelector:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def start(self):
        """
        Get WebDriver Instance based on the browser configuration
        :return 'WebDriver Instance':
        """
        browsers = {
            "CHROME": Chrome(),
            "FIREFOX": Firefox(),
            "EDGE": Edge(),
            "SAFARI": Safari(),
        }
        driver = browsers[self.browser.upper()].start()
        driver.maximize_window()
        driver.get(self.url)
        SeleniumBase(driver).wait_until_page_is_completely_loaded()
        return driver
