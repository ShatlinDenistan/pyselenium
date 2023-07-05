from automation.cookie import Cookie
from automation.frame import Frame
from automation.checks import Checks
from automation.interaction import Interaction
from automation.screenshot import Screenshot
from automation.scroll import Scroll
from automation.selectelement import SelectElement
from automation.tableelement import TableElement
from automation.asserts import Verify

from config.config import LOG_SUMMARY_PATH

from datetime import datetime


class PageBase(
    Checks,
    Interaction,
    Screenshot,
    Scroll,
    SelectElement,
    Frame,
    Cookie,
    TableElement,
    Verify,
):
    def write_to_summary(self, message):
        f = open(LOG_SUMMARY_PATH, "a")
        time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        f.write(f"{time}|{message}\n")
