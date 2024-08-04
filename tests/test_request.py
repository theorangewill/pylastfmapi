from http import HTTPStatus

import pytest

from pylastfm.exceptions import RequestErrorException
from pylastfm.request import RequestController


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


####
# Test request_all_pages
####
def test_request_all_pages(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'parent': {'list': [2], '@attr': {'totalPages': total_pages}}
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ###
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list')
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages


def test_request_all_page_receive_page_with_no_data(mocker, capfd):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for _ in range(total_pages - 1):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            'parent': {'list': [2], '@attr': {'totalPages': total_pages}}
        }
        mock_responses.append(mock_response)
    mock_response = mocker.Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {'parent': {'list': []}}
    mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list')
    ##
    assert mock_request.call_count == 4  # noqa: PLR2004
    assert len(response) == 3  # noqa: PLR2004
    assert (
        'No more results, but there are more pages\n' in capfd.readouterr().out
    )


def test_request_all_page_from_cache(mocker):
    user_agent_test = 'user_agent_test'
    api_key_test = 'api_key_test'
    payload = {'method': 'method-name'}
    total_pages = 4
    # Mock request responses
    mock_responses = []
    for page in range(total_pages):
        mock_response = mocker.Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.from_cache = page % 2 == 0
        mock_response.json.return_value = {
            'parent': {'list': [2], '@attr': {'totalPages': total_pages}}
        }
        mock_responses.append(mock_response)
    mock_request = mocker.patch.object(RequestController, 'request')
    mock_request.side_effect = mock_responses
    ##
    controller = RequestController(user_agent_test, api_key_test)
    ##
    response = controller.request_all_pages(payload, 'parent', 'list')
    ##
    assert mock_request.call_count == total_pages
    assert len(response) == total_pages
