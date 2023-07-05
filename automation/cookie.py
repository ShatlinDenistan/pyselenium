from datetime import datetime
from typing import Union, Optional
from automation.error import CookieNotFound
from automation.selenium_base import SeleniumBase


class Cookie:
    def __init__(
        self,
        name,
        value,
        driver,
        path=None,
        domain=None,
        secure=False,
        http_only=False,
        expiry=None,
        **extra,
    ):
        self.name = name
        self.value = value
        self.driver = driver
        self.path = path
        self.domain = domain
        self.secure = secure
        self.http_only = http_only
        self.expiry = datetime.fromtimestamp(expiry) if expiry else None
        self.extra = extra

    def __str__(self):
        items = "name value path domain secure httpOnly expiry".split()
        string = "\n".join(f"{item}={getattr(self, item)}" for item in items)
        if self.extra:
            string = f"{string}\nextra={self.extra}\n"
        return string


class CookieKeywords(SeleniumBase):
    def delete_all_cookies(self):
        """Deletes all cookies."""
        self.driver.delete_all_cookies()

    def delete_cookie(self, name):
        """Deletes the cookie matching ``name``.

        If the cookie is not found, nothing happens.
        """
        self.driver.delete_cookie(name)

    def get_cookies(self, as_dict: bool = False) -> Union[str, dict]:
        """Returns all cookies of the current page."""
        pairs = [
            f"{cookie['name']}={cookie['value']}"
            for cookie in self.driver.get_cookies()
        ]
        return "; ".join(pairs)

    def get_cookie(self, name: str) -> Cookie:
        """Returns information of cookie with ``name`` as an object.

        If no cookie is found with ``name``, keyword fails. The cookie object
        contains details about the cookie. Attributes available in the object
        are documented in the table below.

        """
        if cookie := self.driver.get_cookie(name):
            return Cookie(**cookie)
        else:
            raise CookieNotFound(f"Cookie with name '{name}' not found.")

    def add_cookie(
        self,
        name: str,
        value: Union[str, bool],
        path: Optional[str] = None,
        domain: Optional[str] = None,
        secure: Optional[bool] = None,
        expiry: Optional[str] = None,
    ):
        """Adds a cookie to your current session."""
        new_cookie = {"name": name, "value": value}
        if path is not None:
            new_cookie["path"] = path
        if domain is not None:
            new_cookie["domain"] = domain
        # Secure must be True or False
        if secure is not None:
            new_cookie["secure"] = secure
        if expiry is not None:
            new_cookie["expiry"] = self._expiry(expiry)
        self.driver.add_cookie(new_cookie)

    def _expiry(self, expiry):
        return int(expiry)
