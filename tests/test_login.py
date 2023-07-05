"""UI automation tests for the Request Demo page"""
import pytest
from pages.login_page import LoginPage


@pytest.mark.regression
class TestLogin:
    """UI automation tests for the Request Demo page"""

    @pytest.mark.set1
    def test_login(self):
        loginpage = LoginPage(self.driver)
        loginpage.login("standard_user", "secret_sauce")
