class PageException(Exception):
    """Base class for exceptions in this module."""


class ElementNotFoundException(PageException):
    """Raise when the element is not found in the page."""


class NotValidLocatorException(PageException):
    """Raise when the locator provided is not valid."""


class ElementNotVisibleException(PageException):
    """Raise when the element is not visible in the page."""


class WindowNotFound(PageException):
    pass


class CookieNotFound(PageException):
    pass


class NoOpenBrowser(PageException):
    pass


class PluginError(PageException):
    pass
