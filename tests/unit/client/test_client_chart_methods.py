from pylastfmapi.constants import (
    CHART_GETTOPARTISTS,
    CHART_GETTOPTAGS,
    CHART_GETTOPTRACKS,
)

# #########################################################################
# # GET CHART ARTISTS
# #########################################################################


def test_get_top_artists(setup_paginated_mock):
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_top_artists()
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPARTISTS}, 'artists', 'artist', None
    )
    assert response == return_value


def test_get_top_artists_with_parameters(setup_paginated_mock):
    amount = 10
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_top_artists(amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPARTISTS}, 'artists', 'artist', amount
    )
    assert response == return_value


# #########################################################################
# # GET CHART TAGS
# #########################################################################


def test_get_top_tags(setup_paginated_mock):
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_top_tags()
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTAGS}, 'tags', 'tag', None
    )
    assert response == return_value


def test_get_top_tags_with_parameters(setup_paginated_mock):
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_top_tags(amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTAGS}, 'tags', 'tag', amount
    )
    assert response == return_value


# #########################################################################
# # GET CHART TRACKS
# #########################################################################


def test_get_top_tracks(setup_paginated_mock):
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_top_tracks()
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTRACKS}, 'tracks', 'track', None
    )
    assert response == return_value


def test_get_top_tracks_with_parameters(setup_paginated_mock):
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_top_tracks(amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': CHART_GETTOPTRACKS}, 'tracks', 'track', amount
    )
    assert response == return_value
