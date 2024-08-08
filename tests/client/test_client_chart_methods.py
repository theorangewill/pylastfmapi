from pylastfm.client import LastFM
from pylastfm.constants import (
    CHART_GETTOPARTISTS,
    CHART_GETTOPTAGS,
    CHART_GETTOPTRACKS,
)

# #########################################################################
# # GET CHART ARTISTS
# #########################################################################


def test_get_top_artists(mocker):
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_top_artists()
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPARTISTS}, 'artists', 'artist', None
    )
    assert response == return_value


def test_get_top_artists_with_parameters(mocker):
    amount = 10
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_top_artists(amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPARTISTS}, 'artists', 'artist', amount
    )
    assert response == return_value


# #########################################################################
# # GET CHART TAGS
# #########################################################################


def test_get_top_tags(mocker):
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_top_tags()
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTAGS}, 'tags', 'tag', None
    )
    assert response == return_value


def test_get_top_tags_with_parameters(mocker):
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_top_tags(amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTAGS}, 'tags', 'tag', amount
    )
    assert response == return_value


# #########################################################################
# # GET CHART TRACKS
# #########################################################################


def test_get_top_tracks(mocker):
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_top_tracks()
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTRACKS}, 'tracks', 'track', None
    )
    assert response == return_value


def test_get_top_tracks_with_parameters(mocker):
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_top_tracks(amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTRACKS}, 'tracks', 'track', amount
    )
    assert response == return_value
