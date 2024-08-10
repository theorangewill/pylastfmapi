from http import HTTPStatus
from unittest.mock import call

import pytest

from pylastfm.constants import LIMIT, LIMIT_SEARCH
from pylastfm.exceptions import RequestErrorException
from pylastfm.request import RequestController

##############################################################################
# Test request
##############################################################################


@pytest.fixture
def mock_request_get(mocker):
    mock_request_get = mocker.patch('requests.get', autospec=True)
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {}
    mock_response.text = 'response text'
    mock_request_get.return_value = mock_response
    return mock_request_get


def test_request_spy(mocker, mock_request_get):
    url_test = 'url-test.com'
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    mocker.patch('pylastfm.request.URL', url_test)
    mocker.patch('requests_cache.install_cache', autospec=True)
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request({
        'param1': 'parameter-test',
        'param2': 'parameter-test-2',
    })
    ##
    assert response.status_code == HTTPStatus.OK
    assert response.text == 'response text'
    mock_request_get.assert_called_once()
    mock_request_get.assert_called_with(
        url_test,
        headers={'user-agent': user_agent_test},
        params={
            'api_key': api_key_test,
            'format': 'json',
            'param1': 'parameter-test',
            'param2': 'parameter-test-2',
        },
    )


def test_request_spy_overide_api_key(mocker, mock_request_get):
    url_test = 'url-test.com'
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    mocker.patch('pylastfm.request.URL', url_test)
    mocker.patch('requests_cache.install_cache', autospec=True)
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request({
        'param1': 'parameter-test',
        'api_key': 'apy_key_test_2',
    })
    ##
    assert response.status_code == HTTPStatus.OK
    assert response.text == 'response text'
    mock_request_get.assert_called_once()
    mock_request_get.assert_called_with(
        url_test,
        headers={'user-agent': user_agent_test},
        params={
            'api_key': 'apy_key_test_2',
            'format': 'json',
            'param1': 'parameter-test',
        },
    )


def test_request_with_status_error(mocker):
    url_test = 'url-test.com'
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    mocker.patch('pylastfm.request.URL', url_test)
    mocker.patch('requests_cache.install_cache', autospec=True)

    mock_request_get = mocker.patch('requests.get', autospec=True)
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.NOT_FOUND
    mock_response.text = 'Error!'
    mock_request_get.return_value = mock_response
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    with pytest.raises(
        RequestErrorException,
        match='Something wrong, HTTP error 404: Error!',
    ):
        _ = controller.request({'param1': 'parameter-test'})


def test_request_with_error_message(mocker):
    url_test = 'url-test.com'
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    mocker.patch('pylastfm.request.URL', url_test)
    mocker.patch('requests_cache.install_cache', autospec=True)

    mock_request_get = mocker.patch('requests.get', autospec=True)
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {'error': '6', 'message': 'Error!'}
    mock_request_get.return_value = mock_response
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    with pytest.raises(
        RequestErrorException,
        match='Something wrong, error 6: Error!',
    ):
        _ = controller.request({'param1': 'parameter-test'})


##############################################################################
# Test request_all_pages
##############################################################################
def test_request_all_pages(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * LIMIT,
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['parent']['list'])
    assert len(_list) == amount


def test_request_all_pages_receive_page_with_no_data(mocker, capfd):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages - 1):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * LIMIT,
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {
        'parent': {'list': [], '@attr': {'totalPages': total_pages}}
    }
    mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == 4  # noqa: PLR2004
    assert len(response) == 3  # noqa: PLR2004
    _list = []
    for r in response:
        _list.extend(r.json()['parent']['list'])
    assert len(_list) == amount - LIMIT


def test_request_all_pages_from_cache(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * LIMIT,
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['parent']['list'])
    assert len(_list) == amount


def test_request_all_pages_amount_lower_than_limit(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    amount = LIMIT - 1
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * amount,
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == 1  # noqa: PLR2004
    mock_request.assert_has_calls([
        call({'method': 'method-name', 'limit': amount, 'page': 1})
    ])
    assert len(response) == 1  # noqa: PLR2004
    _list = []
    for r in response:
        _list.extend(r.json()['parent']['list'])
    assert len(_list) == amount


def test_request_all_pages_amount_higher_than_limit_lower_than_total(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    amount = LIMIT * 3 - 1
    # Mock request responses
    mock_responses = []
    for page in range(total_pages - 2):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * LIMIT,
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    for page in range(total_pages - 2):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * (amount % LIMIT),
                '@attr': {'totalPages': total_pages},
            }
        }
    mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == 3  # noqa: PLR2004
    mock_request.assert_has_calls(
        [
            call({'method': 'method-name', 'limit': LIMIT, 'page': 1}),
            call({'method': 'method-name', 'limit': LIMIT, 'page': 2}),
            call({
                'method': 'method-name',
                'limit': amount % LIMIT,
                'page': 3,
            }),
        ],
    )
    assert len(response) == 3  # noqa: PLR2004
    _list = []
    for r in response:
        _list.extend(r.json()['parent']['list'])
    assert len(_list) == amount


def test_request_all_pages_amount_higher_than_limit_higher_than_total(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    amount = LIMIT * 10 - 1
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'parent': {
                'list': [2] * LIMIT,
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == total_pages
    mock_request.assert_has_calls(
        [
            call({'method': 'method-name', 'limit': LIMIT, 'page': 1}),
            call({'method': 'method-name', 'limit': LIMIT, 'page': 2}),
            call({'method': 'method-name', 'limit': LIMIT, 'page': 3}),
            call({'method': 'method-name', 'limit': LIMIT, 'page': 4}),
        ],
    )
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['parent']['list'])
    assert len(_list) == LIMIT * total_pages


def test_request_all_pages_with_tagging(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'taggings': {
                'parent': {
                    'list': [2] * LIMIT,
                },
                '@attr': {'totalPages': total_pages},
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list', amount)
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['taggings']['parent']['list'])
    assert len(_list) == amount


##############################################################################
# Test request_search_pages
##############################################################################


def test_request_search_pages(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT_SEARCH * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'results': {
                'parent': {
                    'list': [2] * LIMIT_SEARCH,
                },
                'opensearch:totalResults': amount,
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_search_pages(
        payload, 'parent', 'list', amount
    )
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['results']['parent']['list'])
    assert len(_list) == amount


def test_request_search_pages_receive_page_with_no_data(mocker, capfd):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT_SEARCH * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages - 1):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'results': {
                'parent': {
                    'list': [2] * LIMIT_SEARCH,
                },
                'opensearch:totalResults': total_pages * LIMIT_SEARCH,
            }
        }
        mock_responses.append(mock_response)
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {
        'results': {
            'parent': {'list': [], '@attr': {'totalPages': total_pages}},
            'opensearch:totalResults': total_pages * LIMIT_SEARCH,
        }
    }
    mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_search_pages(
        payload, 'parent', 'list', amount
    )
    ##
    assert mock_request.call_count == 4  # noqa: PLR2004
    assert len(response) == 3  # noqa: PLR2004
    _list = []
    for r in response:
        _list.extend(r.json()['results']['parent']['list'])
    assert len(_list) == amount - LIMIT_SEARCH


def test_request_search_pages_from_cache(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    amount = LIMIT_SEARCH * 4
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'results': {
                'parent': {
                    'list': [2] * LIMIT_SEARCH,
                },
                'opensearch:totalResults': amount,
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_search_pages(
        payload, 'parent', 'list', amount
    )
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['results']['parent']['list'])
    assert len(_list) == amount


def test_request_search_pages_amount_lower_than_limit(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    amount = LIMIT_SEARCH - 1
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'results': {
                'parent': {
                    'list': [2] * LIMIT_SEARCH,
                },
                'opensearch:totalResults': LIMIT_SEARCH * total_pages,
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_search_pages(
        payload, 'parent', 'list', amount
    )
    ##
    assert mock_request.call_count == 1  # noqa: PLR2004
    mock_request.assert_has_calls([
        call({'method': 'method-name', 'limit': amount, 'page': 1})
    ])
    assert len(response) == 1  # noqa: PLR2004
    _list = []
    for r in response:
        _list.extend(r.json()['results']['parent']['list'])
    assert len(_list) == LIMIT_SEARCH


def test_request_search_pages_amount_higher_than_limit_lower_than_total(
    mocker,
):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    amount = LIMIT_SEARCH * 3 - 1
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'results': {
                'parent': {
                    'list': [2] * LIMIT_SEARCH,
                },
                'opensearch:totalResults': total_pages * LIMIT_SEARCH,
            }
        }
        mock_responses.append(mock_response)
    mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_search_pages(
        payload, 'parent', 'list', amount
    )
    ##
    assert mock_request.call_count == 3  # noqa: PLR2004
    mock_request.assert_has_calls(
        [
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 1}),
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 2}),
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 3}),
        ],
    )
    assert len(response) == 3  # noqa: PLR2004
    _list = []
    for r in response:
        _list.extend(r.json()['results']['parent']['list'])
    assert len(_list) == LIMIT_SEARCH * 3


def test_request_search_pages_amount_higher_than_limit_higher_than_total(
    mocker,
):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    amount = LIMIT_SEARCH * 10 - 1
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'results': {
                'parent': {
                    'list': [2] * LIMIT_SEARCH,
                },
                'opensearch:totalResults': total_pages * LIMIT_SEARCH,
            }
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_search_pages(
        payload, 'parent', 'list', amount
    )
    ##
    assert mock_request.call_count == total_pages
    mock_request.assert_has_calls(
        [
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 1}),
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 2}),
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 3}),
            call({'method': 'method-name', 'limit': LIMIT_SEARCH, 'page': 4}),
        ],
    )
    assert len(response) == total_pages
    _list = []
    for r in response:
        _list.extend(r.json()['results']['parent']['list'])
    assert len(_list) == LIMIT_SEARCH * total_pages


##############################################################################
# Test clear_cache
##############################################################################


def test_controller_with_clear_cache_flag(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    reset_cache = True
    mocker.patch('requests_cache.install_cache', autospec=True)
    mock_clear_cache = mocker.patch.object(RequestController, 'clear_cache')
    ###
    _ = RequestController(user_agent_test, api_key_test, reset_cache)
    ##
    mock_clear_cache.assert_called_once()


def test_clear_cache_(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    mocker.patch('requests_cache.install_cache', autospec=True)
    mock_cache = mocker.Mock()
    mock_cache.clear.return_value = None
    mock_get_cache = mocker.patch('requests_cache.get_cache', autospec=True)
    mock_get_cache.return_value = mock_cache
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    _ = controller.clear_cache()
    ##
    mock_get_cache.assert_called_once()
