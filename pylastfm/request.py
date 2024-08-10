import time
from http import HTTPStatus
from math import ceil
from typing import Annotated

import requests
import requests_cache

from pylastfm.constants import LIMIT, LIMIT_SEARCH, URL
from pylastfm.exceptions import RequestErrorException

T_Response = Annotated[
    requests_cache.models.response.OriginalResponse,
    requests_cache.models.response.CachedResponse,
]


class RequestController:
    def __init__(
        self, user_agent: str, api_key: str, reset_cache: bool = False
    ) -> None:
        self.headers = {'user-agent': user_agent}
        self.payload = {'api_key': api_key, 'format': 'json'}
        requests_cache.install_cache()
        if reset_cache:
            self.clear_cache()

    def request(self, payload: dict) -> T_Response:
        self.payload.update(payload)
        response = requests.get(URL, headers=self.headers, params=self.payload)

        if response.status_code != HTTPStatus.OK:
            raise RequestErrorException(
                f'Something wrong, HTTP error {response.status_code}: '
                f'{response.text}'
            )

        content = response.json()
        if 'error' in content:
            raise RequestErrorException(
                f'Something wrong, error {content["error"]}: '
                f'{content["message"]}'
            )
        return response

    @staticmethod
    def clear_cache() -> None:
        cache = requests_cache.get_cache()
        cache.clear()

    def request_all_pages(
        self, payload: dict, parent_key: str, list_key: str, amount: int
    ) -> list[T_Response]:
        responses = []
        page = 1
        num_pages = None

        payload['limit'] = LIMIT
        if amount:
            if amount < LIMIT:
                last_limit = amount
                num_pages = 1
            else:
                last_limit = amount % LIMIT
                num_pages = ceil(amount / LIMIT)

        while True:
            payload = {**payload, 'page': page}
            if num_pages == page:
                payload.update({'limit': last_limit})
            response = self.request(payload)
            content = response.json()

            if (
                len(content.get('taggings', content)[parent_key][list_key])
                == 0
            ):
                break
            if not getattr(response, 'from_cache', False):
                time.sleep(0.25)
            responses.append(response)
    
            if 'taggings' in content:
                if page == int(content['taggings']['@attr']['totalPages']):
                    break
            else:
                if page == int(content[parent_key]['@attr']['totalPages']):
                    break

            if num_pages and page == num_pages:
                break

            page += 1
        return responses

    def request_search_pages(
        self, payload: dict, parent_key: str, list_key: str, amount: int
    ) -> list[T_Response]:
        responses = []
        page = 1
        num_pages = None

        payload['limit'] = LIMIT_SEARCH
        if amount:
            if amount < LIMIT_SEARCH:
                num_pages = 1
                payload['limit'] = amount
            else:
                num_pages = ceil(amount / LIMIT_SEARCH)

        while True:
            payload = {**payload, 'page': page}
            response = self.request(payload)
            content = response.json()

            if len(content['results'][parent_key][list_key]) == 0:
                break
            if not getattr(response, 'from_cache', False):
                time.sleep(0.25)
            responses.append(response)

            if page == ceil(
                int(content['results']['opensearch:totalResults'])
                / LIMIT_SEARCH
            ):
                break
            if num_pages and page == num_pages:
                break

            page += 1
        return responses
