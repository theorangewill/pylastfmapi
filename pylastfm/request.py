import time
from http import HTTPStatus
from math import ceil
from typing import Annotated

import requests
import requests_cache

from pylastfm.constants import LIMIT, LIMIT_SEARCH, URL
from pylastfm.exceptions import RequestErrorException

# T_Response is a type alias representing the possible response types
# returned by requests made through the `RequestController`.
# It can be either an original
# response from the LastFM API or a cached response stored by requests_cache.
T_Response = Annotated[
    requests_cache.models.response.Response,
    requests_cache.models.response.OriginalResponse,
    requests_cache.models.response.CachedResponse,
]


class RequestController:
    """Handles API requests and manages cached responses for the LastFM API."""

    def __init__(
        self, user_agent: str, api_key: str, reset_cache: bool = False
    ) -> None:
        """Initializes the RequestController with user-agent and API key.

        Args:
            user_agent (str): The user-agent string to be sent with
                each request.
            api_key (str): The API key for authentication with the LastFM API.
            reset_cache (bool, optional): If True, clears the existing cache.
                Defaults to False.
        """
        self.headers = {'user-agent': user_agent}
        self.payload = {'api_key': api_key, 'format': 'json'}
        requests_cache.install_cache()
        if reset_cache:
            self.clear_cache()

    def request(self, payload: dict) -> T_Response:
        """Sends a request to the LastFM API and returns the response.

        Args:
            payload (dict): The query parameters for the request.

        Returns:
            T_Response: The HTTP response object, which may be cached.

        Raises:
            RequestErrorException: If the response status code is not
                200 (OK) or if the response contains an error.
        """
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
        """Clears the cache of stored API responses."""
        cache = requests_cache.get_cache()
        if cache:
            cache.clear()

    #########################################################################
    # PAGINATION
    #########################################################################

    def request_all_pages(
        self, payload: dict, parent_key: str, list_key: str, amount: int | None
    ) -> list[T_Response]:
        """Requests all pages of data from the API for a given query,
        handling pagination.

        Args:
            payload (dict): The query parameters for the request.
            parent_key (str): The parent key in the JSON response
                containing the desired data.
            list_key (str): The key within the parent key's value
                that contains the list of items.
            amount (int): The total number of items to request.

        Returns:
            list[T_Response]: A list of HTTP response objects,
                each representing a page of data.
        """
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
            elif page == int(content[parent_key]['@attr']['totalPages']):
                break

            if num_pages and page == num_pages:
                break

            page += 1
        return responses

    def get_paginated_data(
        self, payload: dict, parent_key: str, list_key: str, amount: int | None
    ) -> list[dict]:
        """Fetches paginated data from the LastFM API based on the
        given parameters.

        This method handles the pagination of API requests to gather a
        specified amount
        of data, combining the results into a single list.

        Args:
            payload (dict): The parameters to send to the API.
            parent_key (str): The key in the API response that contains the
                primary data structure.
            list_key (str): The key within the `parent_key` that contains
                the list of items.
            amount (int): The total number of elements to retrieve from
                the API.

        Returns:
            list[dict]: A list of dictionaries containing the retrieved data.
        """
        responses = self.request_all_pages(
            payload, parent_key, list_key, amount
        )
        response_list = []
        for data in responses:
            _data = data.json()
            response_list.extend(
                _data.get('taggings', _data)[parent_key][list_key]
            )
        return response_list

    #########################################################################
    # SEARCHES
    #########################################################################

    def request_search_pages(
        self, payload: dict, parent_key: str, list_key: str, amount: int | None
    ) -> list[T_Response]:
        """Requests all pages of data from the API for a given query,
        handling pagination. Specific for LastFM search format.

        Args:
            payload (dict): The query parameters for the search request.
            parent_key (str): The parent key in the JSON response
            containing the search results.
            list_key (str): The key within the parent key's value
            that contains the list of items.
            amount (int): The total number of items to request.

        Returns:
            list[T_Response]: A list of HTTP response objects,
            each representing a page of search results.
        """
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

    def get_search_data(
        self, payload: dict, parent_key: str, list_key: str, amount: int | None
    ) -> list[dict]:
        """Fetches search result data from the LastFM API based on the
        given parameters.

        This method handles the pagination of search result requests,
        retrieving
        the specified number of results and combining them into a single list.

        Args:
            payload (dict): The parameters to send to the API for the
                search request.
            parent_key (str): The key in the API response that contains
                the primary data structure.
            list_key (str): The key within the `parent_key` that contains
                the list of items.
            amount (int): The total number of elements to retrieve from
                the API.

        Returns:
            list[dict]: A list of dictionaries containing the search results.
        """
        responses = self.request_search_pages(
            payload, parent_key, list_key, amount
        )
        response_list = []
        for index, data in enumerate(responses, start=1):
            if amount and index == len(responses):
                left_data = amount % LIMIT_SEARCH
                response_list.extend(
                    data.json()['results'][parent_key][list_key][:left_data]
                )
            else:
                response_list.extend(
                    data.json()['results'][parent_key][list_key]
                )
        return response_list
