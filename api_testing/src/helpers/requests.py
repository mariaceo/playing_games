from dataclasses import dataclass

import requests


@dataclass
class Response:
    status_code: int
    text: str
    body: object
    headers: dict


class APIRequest:
    def get(self, url):
        response = requests.get(url)
        return self.__get_responses(response)

    def post(self, url, payload=None, headers=None):
        response = requests.post(url, data=payload, headers=headers)
        return self.__get_responses(response)

    def delete(self, url):
        response = requests.delete(url)
        return self.__get_responses(response)

    def __get_responses(self, response):
        status_code = response.status_code
        text = response.text

        try:
            body = response.json()
        except Exception:
            body = {}

        headers = response.headers

        return Response(
            status_code, text, body, headers
        )