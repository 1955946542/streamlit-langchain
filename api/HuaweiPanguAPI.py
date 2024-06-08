# api.py
import requests
from langchain.schema import HumanMessage, AIMessage

class HuaweiPanguAPI:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = self.get_access_token()

    def get_access_token(self):
        url = "https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "auth": {
                "identity": {
                    "methods": ["api"],
                    "api": {
                        "name": self.api_key,
                        "password": self.api_secret
                    }
                }
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 201:
            return response.headers.get("X-Subject-Token")
        else:
            raise Exception(f"Failed to get access token: {response.status_code}, {response.text}")

    def __call__(self, messages: [HumanMessage]):
        url = "https://nlp.cn-north-4.myhuaweicloud.com/v1/nlp/text-generation"
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.token
        }
        payload = {
            "text": messages[-1].content,
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            ai_response = response.json().get("generated_text")
            return AIMessage(content=ai_response)
        else:
            raise Exception(f"Failed to get response from Huawei Pangu API: {response.status_code}, {response.text}")
