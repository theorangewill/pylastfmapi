from pylastfm.client import LastFM
from pylastfm.constants import (
    GEO_GETOPTRACKS,
    GEO_GETTOPARTISTS,
)

# #########################################################################
# # GET COUNTRY TOP ARTISTS
# #########################################################################


def test_get_country_top_artists(mocker):
    country = 'countryname'
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_country_top_artists(country=country)
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': GEO_GETTOPARTISTS, 'country': country},
        'topartists',
        'artist',
        None,
    )
    assert response == return_value


def test_get_country_top_artists_with_parameters(mocker):
    country = 'countryname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_country_top_artists(country=country, amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': GEO_GETTOPARTISTS, 'country': country},
        'topartists',
        'artist',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET COUNTRY TOP TRACKS
# #########################################################################


def test_get_country_top_tracks(mocker):
    country = 'countryname'
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_country_top_tracks(country=country)
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': GEO_GETOPTRACKS, 'country': country, 'location': None},
        'tracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_country_top_tracks_with_parameters(mocker):
    country = 'countryname'
    location = 'locationname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_country_top_tracks(
        country=country, location=location, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
        {'method': GEO_GETOPTRACKS, 'country': country, 'location': location},
        'tracks',
        'track',
        amount,
    )
    assert response == return_value
