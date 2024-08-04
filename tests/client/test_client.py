from pylastfm.client import LastFM


def test_get_paginated_data(mocker):
    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value

    amount_responses = 5
    payload = {'method': 'test'}
    parent_key = 'parent'
    list_key = 'list'
    amount = 5

    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = {
        parent_key: {list_key: [{'name': 'item1'}, {'name': 'item2'}]}
    }
    mock_responses = [mock_response] * amount_responses
    mock_request_controller.request_all_pages.return_value = mock_responses

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_paginated_data(payload, parent_key, list_key, amount)
    ##
    mock_request_controller.request_all_pages.assert_called_once()
    mock_request_controller.request_all_pages.assert_called_with(
        payload, parent_key, list_key, amount
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
