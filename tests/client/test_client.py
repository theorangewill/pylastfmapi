from pylastfm.client import LastFM
from pylastfm.constants import (
    CHART_GETTOPARTISTS,
    CHART_GETTOPTAGS,
    CHART_GETTOPTRACKS,
    LIMIT,
)


def test_get_paginated_data(mocker):
    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value

    amount_responses = 5
    payload = {'method': 'test'}
    parent_key = 'parent'
    list_key = 'list'

    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = {
        parent_key: {list_key: [{'name': 'item1'}, {'name': 'item2'}]}
    }
    mock_responses = [mock_response] * amount_responses
    mock_request_controller.request_all_pages.return_value = mock_responses

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_paginated_data(payload, parent_key, list_key)
    ##
    mock_request_controller.request_all_pages.assert_called_once()
    mock_request_controller.request_all_pages.assert_called_with(
        payload, parent_key, list_key
    )
    assert response == [
        {'name': 'item1'},
        {'name': 'item2'},
        {'name': 'item1'},
        {'name': 'item2'},
        {'name': 'item1'},
        {'name': 'item2'},
        {'name': 'item1'},
        {'name': 'item2'},
        {'name': 'item1'},
        {'name': 'item2'},
    ]


def test_get_top_artists(mock_lastfm_client_with_get_paginated_data):
    client, mock_get_paginated_data = (
        mock_lastfm_client_with_get_paginated_data
    )
    payload = {'method': CHART_GETTOPARTISTS, 'limit': LIMIT}
    parent_key = 'artists'
    list_key = 'artist'

    ##
    response = client.get_top_artists()
    ##
    mock_get_paginated_data.assert_called_once()
    mock_get_paginated_data.assert_called_with(payload, parent_key, list_key)
    assert response == [{'name': 'item1'}, {'name': 'item2'}]


def test_get_top_tags(mock_lastfm_client_with_get_paginated_data):
    client, mock_get_paginated_data = (
        mock_lastfm_client_with_get_paginated_data
    )
    payload = {'method': CHART_GETTOPTAGS, 'limit': LIMIT}
    parent_key = 'tags'
    list_key = 'tag'
    ##
    response = client.get_top_tags()
    ##
    mock_get_paginated_data.assert_called_once()
    mock_get_paginated_data.assert_called_with(payload, parent_key, list_key)
    assert response == [{'name': 'item1'}, {'name': 'item2'}]


def test_get_top_tracks(mock_lastfm_client_with_get_paginated_data):
    client, mock_get_paginated_data = (
        mock_lastfm_client_with_get_paginated_data
    )
    payload = {'method': CHART_GETTOPTRACKS, 'limit': LIMIT}
    parent_key = 'tracks'
    list_key = 'track'
    ##
    response = client.get_top_tracks()
    ##
    mock_get_paginated_data.assert_called_once()
    mock_get_paginated_data.assert_called_with(payload, parent_key, list_key)
    assert response == [{'name': 'item1'}, {'name': 'item2'}]
