TEST_DATA_URL = {"products": "get_products/active/10"}
BASE_URL = "http://tal-test-data-service.master.env/"


class BaseData:
    def get_request(self, url):
        return {
            "header": {},
            "data": {},
            "baseurl": BASE_URL,
            "url": f"{BASE_URL}{TEST_DATA_URL[url]}",
        }
