from pylastfmapi.constants import (
    GEO_GETOPTRACKS,
    GEO_GETTOPARTISTS,
)

# #########################################################################
# # GET COUNTRY TOP ARTISTS
# #########################################################################


def test_get_country_top_artists(setup_paginated_mock):
    country = 'countryname'
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_country_top_artists(country=country)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': GEO_GETTOPARTISTS, 'country': country},
        'topartists',
        'artist',
        None,
    )
    assert response == return_value


def test_get_country_top_artists_with_parameters(setup_paginated_mock):
    country = 'countryname'
    amount = 10
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_country_top_artists(country=country, amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': GEO_GETTOPARTISTS, 'country': country},
        'topartists',
        'artist',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET COUNTRY TOP TRACKS
# #########################################################################


def test_get_country_top_tracks(setup_paginated_mock):
    country = 'countryname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_country_top_tracks(country=country)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': GEO_GETOPTRACKS, 'country': country, 'location': None},
        'tracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_country_top_tracks_with_parameters(setup_paginated_mock):
    country = 'countryname'
    location = 'locationname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_country_top_tracks(
        country=country, location=location, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': GEO_GETOPTRACKS, 'country': country, 'location': location},
        'tracks',
        'track',
        amount,
    )
    assert response == return_value
