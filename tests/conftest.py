import pytest

from pylastfm.client import LastFM


@pytest.fixture
def mock_lastfm_client_with_get_paginated_data(mocker):
    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=[{'name': 'item1'}, {'name': 'item2'}],
    )
    client = LastFM('user_agent_test', 'api_key_test')
    return client, mock_get_paginated_data
