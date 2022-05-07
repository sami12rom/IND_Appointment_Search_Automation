import json
from typing import Dict

import requests
import urllib3


class RESTAPI:

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def __init__(self):
        self.headers = {"Accept": "*/*",
                        "User-Agent": "Mozilla/5.0",
                        "Content-Type": "application/json"}

    def get_authorization_token(self, url: str, method: str, token_name: str = '',  # nosec
                                headers: Dict = None, data: Dict = None):

        if headers is None:
            headers = {}
        if data is None:
            data = {}

        try:
            api_call = requests.request(url=url, method=method, headers={**self.headers, **headers},
                                        data=data, verify=False)
            content = json.loads(api_call.content.decode("utf-8"))
            if token_name == '':
                print(f"Error: Specify token_name from results &/or : {content}")  # nosec
            else:
                token = content[token_name]
                print(api_call)
                return token

        except Exception as e:
            print(f"Error: {e}")

    def api_call(self, url: str, method: str, headers: Dict = None, data: Dict = None):

        if headers is None:
            headers = {}
        if data is None:
            data = {}

        try:
            api_call = requests.request(url=url, method=method, headers={**self.headers, **headers},
                                        data=data, verify=False)
            content = api_call.content.decode("utf-8")
            print(api_call)
            return content

        except Exception as e:
            print(f"Error: {e}")
