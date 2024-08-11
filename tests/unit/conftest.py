import pytest

from pylastfm.client import LastFM


@pytest.fixture
def setup_request_mock(mocker):
    def _setup_request_mock(return_value):
        MockRequestController = mocker.patch(
            'pylastfm.client.RequestController', autospec=True
        )
        mock_request_controller = MockRequestController.return_value
        mock_response = mocker.Mock().return_value
        mock_response.json.return_value = return_value
        mock_request_controller.request.return_value = mock_response

        client = LastFM('user_agent_test', 'api_key_test')
        return client, mock_request_controller

    return _setup_request_mock


@pytest.fixture
def setup_paginated_mock(mocker):
    def _setup_paginated_mock(return_value):
        MockRequestController = mocker.patch(
            'pylastfm.client.RequestController', autospec=True
        )
        mock_request_controller = MockRequestController.return_value
        mock_request_controller.get_paginated_data.return_value = return_value
        client = LastFM('user_agent_test', 'api_key_test')
        return client, mock_request_controller

    return _setup_paginated_mock


@pytest.fixture
def setup_search_mock(mocker):
    def _setup_search_mock(return_value):
        MockRequestController = mocker.patch(
            'pylastfm.client.RequestController', autospec=True
        )
        mock_request_controller = MockRequestController.return_value
        mock_request_controller.get_search_data.return_value = return_value
        client = LastFM('user_agent_test', 'api_key_test')
        return client, mock_request_controller

    return _setup_search_mock
