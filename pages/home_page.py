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


class HomePage(PageBase):
    def is_in_home_page(self):
        self.wait_until_element_is_visible(HomePO.login_link, 40)
        return True

    def verify_framework(self):
        try:
            self.wait_until_page_contains_text("Login")
            self.wait_until_page_contains_text("Register")
            self.wait_until_page_contains_text("Orders")
            # wait_until_page_contains_text("Shatlin")
            self.wait_until_page_contains_element(HomePO.got_it_btn)
            # self.wait_until_page_contains_element(HomePO.breadcrumb_links)
        except Exception as e:
            logger.info(str(e))

    def handle_cookie(self) -> bool:
        self.wait_until_page_is_completely_loaded()
        if self.element_exists(HomePO.got_it_btn, 3):
            self.click_element(HomePO.got_it_btn)
            return True
        return False

    def get_total_categories(self, dept_index) -> int:
        dept_locator = f"{HomePO.dept_lists}[{dept_index}]"
        self.hover(dept_locator)
        categories = self.get_child_elements(HomePO.cat_head, HomePO.cat_links)
        return len(categories) + 1

    def is_dept_index_greater_than_total_depts(self, dept_index) -> bool:
        departments = self.get_child_elements(HomePO.dept_head, HomePO.dept_lists)
        total_depts = len(departments)
        return dept_index > total_depts

    def walk_department(self, dept_index) -> str:
        dept_locator = f"{HomePO.dept_lists}[{dept_index}]"
        self.hover(dept_locator)
        department = self.get_text(dept_locator)
        logger.info(f"hovered over department {dept_index}. {department}")
        return department

    def walk_category(self, cats_visited) -> str:
        cat_locator = f"({HomePO.cat_links})[{cats_visited}]"
        category = self.get_text(cat_locator).replace("\n", " ")
        logger.info(f"    Clicking Category {cats_visited}. {category}")
        self.click_element(cat_locator)
        return category

    nodes_walked = 0

    def walk_node(self, dept, cat) -> None:
        self.wait_until_page_is_completely_loaded()
        counter = 1
        tabs = ""
        while True:
            try:
                node_link = HomePO.cat_sublinks

                if not self.element_exists(node_link, 2):
                    node_link = HomePO.cat_sublinks_alt
                    if not self.element_exists(node_link, 2):
                        break
                node = self.get_text(node_link)
                tabs = "\t" * counter
                logger.info(f"{tabs}Clicking node {counter}. {node}")
                counter += 1
                self.click_element(node_link)
                breadcrumb = self.get_breadcrumbs()
                cat_list = self.get_category_list()
                self.nodes_walked += 1
                self._process_walk_node_result([dept, cat, breadcrumb, cat_list])
            except (
                StaleElementReferenceException,
                ElementNotVisibleException,
                ElementClickInterceptedException,
            ):
                counter -= 1
                time.sleep(3)

    def get_breadcrumbs(self) -> List[str]:
        if not self.element_exists(HomePO.breadcrumb_links):
            return []
        breadcrumbs = self.get_elements(HomePO.breadcrumb_links)
        return [self.get_text(x) for x in breadcrumbs]

    def get_category_list(self) -> List[str]:
        if not self.element_exists(HomePO.cat_list):
            return []
        cat_text = self.get_text(HomePO.cat_list)
        return cat_text.replace("All Categories\n", "").split("\n")

    def perform_tree_walk(self, dept_index):
        self.go_to(BASE_URL)
        if self.is_dept_index_greater_than_total_depts(dept_index):
            return
        visited_category_count = 1
        total_categories = self.get_total_categories(dept_index)
        cookie_handled = False
        while visited_category_count < total_categories:
            logger.info("=" * 100)
            dept = self.walk_department(dept_index)
            cat = self.walk_category(visited_category_count)
            if cookie_handled is False:
                cookie_handled = self.handle_cookie()
            self.walk_node(dept, cat)
            visited_category_count += 1
            self.go_to(BASE_URL)

    def _process_walk_node_result(self, result):
        dept = result[0]
        category = result[1]
        breadcrumb = result[2]
        categories = result[3]
        node = result[2][-1] if breadcrumb else ""
        result = "pass" if set(breadcrumb).issubset(set(categories)) else "fail"
        logger.info(f"{breadcrumb=}")
        logger.info(f"{categories=}")
        logger.info(f"{result}")
        time = datetime.now().strftime("%d-%m-%Y %H:%S")
        self.write_to_summary(
            f"{time}|{self.nodes_walked}|{breadcrumb}|{categories}|{result}"
        )
        self.take_screenshot(f"{self.nodes_walked}_{result}_{dept}_{category}_{node}")
