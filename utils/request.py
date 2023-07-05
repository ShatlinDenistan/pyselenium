import json

class RequestUtils(object):

    """All utilties for making API Requests"""

    def __init__(self, session):
        self.session = session["session"]
        self.header = session["header"]
        self.data = session["data"]
        self.response = None
        self.status_code = None
        self.expected_status_code = None
        self.url = ""

    def assert_status_code(self):
        # logger.info(f'url: {self.url} response :{self.response.text}')
        assert self.status_code == self.expected_status_code, (
            f"bad status code "
            f" expected status code {self.expected_status_code}, actual status code {self.status_code} "
            f" URL:{self.url} Response JSON: {self.response}"
        )

    def post(self,endpoint,payload=None,headers=None,expected_status_code=200):
        if not headers:
            headers={"Content-Type":"application/json"}
        self.url=self.base_url+endpoint
        response=self.session.post(url=self.url,data=json.dumps(payload),headers=headers,auth=self.auth)
        self.response=response.json()
        self.status_code=response.status_code
        self.expected_status_code=expected_status_code
        self.assert_status_code()
        return self.response

    def get(
        self, url, payload=None, files=None, headers=None, expected_status_code=200
    ):
        if headers is None:
            headers = self.header
        if payload is None:
            payload = self.data
        self.url = url
        self.response = self.session.get(
            url, data=payload, files=files, headers=headers
        )
        self.status_code = self.response.status_code
        self.expected_status_code = expected_status_code
        self.assert_status_code()
        return self.response
