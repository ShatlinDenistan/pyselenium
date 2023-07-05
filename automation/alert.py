from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from automation.selenium_base import SeleniumBase
from automation.wait_times import DEFAULT
from selenium.webdriver.remote.webelement import WebElement


class AlertKeywords(SeleniumBase):
    ACCEPT = "ACCEPT"
    DISMISS = "DISMISS"
    LEAVE = "LEAVE"
    _next_alert_action = ACCEPT

    def input_text_into_alert(
        self, text: str, action: str = ACCEPT, timeout: int = DEFAULT
    ):
        """Types the given ``text`` into an input field in an alert.

        The alert is accepted by default, but that behavior can be controlled
        by using the ``action`` argument same way as with `Handle Alert`.

        ``timeout`` specifies how long to wait for the alert to appear.
        If it is not given, the global  `DEFAULT` is used instead.
        """
        alert = self._wait_alert(timeout)
        alert.send_keys(text)
        self._handle_alert(alert, action)

    def generate_alert(self, mesage):
        self.driver.execute_script(f"alert('{mesage}')")

    def alert_should_be_present(
        self,
        text: str = "",
        action: str = ACCEPT,
        timeout: int = DEFAULT,
    ):
        """Verifies that an alert is present and by default, accepts it.

        Fails if no alert is present. If ``text`` is a non-empty string,
        then it is used to verify alert's message. The alert is accepted
        by default, but that behavior can be controlled by using the
        ``action`` argument same way as with `Handle Alert`.

        ``timeout`` specifies how long to wait for the alert to appear.
        If it is not given, the global default `DEFAULT` is used instead.
        """
        message = self.handle_alert(action, timeout)
        if text and text != message:
            raise AssertionError(
                f"Alert message should have been '{text}' but it was '{message}'."
            )

    def alert_should_not_be_present(self, action: str = ACCEPT, timeout=DEFAULT):
        """Verifies that no alert is present.

        If the alert actually exists, the ``action`` argument determines
        how it should be handled. By default, the alert is accepted, but
        it can be also dismissed or left open the same way as with the
        `Handle Alert` keyword.

        ``timeout`` specifies how long to wait for the alert to appear.
        By default, is not waited for the alert at all, but a custom time can
        be given if alert may be delayed.

        """
        try:
            alert = self._wait_alert(timeout)
        except AssertionError:
            return
        text = self._handle_alert(alert, action)
        raise AssertionError(f"Alert with message '{text}' present.")

    def handle_alert(self, action: str = ACCEPT, timeout: int = DEFAULT):
        """Handles the current alert and returns its message.

        By default, the alert is accepted, but this can be controlled
        with the ``action`` argument that supports the following
        case-insensitive values:

        - ``ACCEPT``: Accept the alert i.e. press ``Ok``. Default.
        - ``DISMISS``: Dismiss the alert i.e. press ``Cancel``.
        - ``LEAVE``: Leave the alert open.

        The ``timeout`` argument specifies how long to wait for the alert
        to appear. If it is not given, the global default `DEFAULT` is used
        instead.
        """
        alert = self._wait_alert(timeout)
        return self._handle_alert(alert, action)

    def _handle_alert(self, alert, action):
        action = action.upper()
        text = " ".join(alert.text.splitlines())
        if action == self.ACCEPT:
            alert.accept()
        elif action == self.DISMISS:
            alert.dismiss()
        elif action != self.LEAVE:
            raise ValueError(f"Invalid alert action '{action}'.")
        return text

    def _wait_alert(self, timeout=DEFAULT) -> WebElement:
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.alert_is_present())
        except TimeoutException as e:
            raise AssertionError(f"Alert not found in {timeout} seconds.") from e
        except WebDriverException as err:
            raise AssertionError(
                f"An exception occurred waiting for alert: {err}"
            ) from err
