class HomePO:
    """Page Objects for Home Page"""

    login_link = "//a[text()='Login']"
    dept_head = "//ul[contains(@class,'department-categories')]"
    dept_lists = "//ul[contains(@class,'department-categories')]/li"
    cat_head = "//div[contains(@class,'department-flyout-module_container')]"
    cat_links = f"{cat_head}//li//a"
    cat_sublinks = "(//div[@class='list-item sub'])[1]"
    cat_sublinks_alt = "(//a[@class='list-nav-item  context-nav-link'])[1]"
    breadcrumbs = "//div[contains(@class,'breadcrumbs')]"
    breadcrumb_links = "//div[contains(@class,'breadcrumbs')]//a"
    cat_list = "//div[contains(@class,'transition-horizontal-module_slide')]"
    got_it_btn = "//button[text()='Got it']"
