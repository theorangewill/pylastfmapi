from pylastfm.client import LastFM
from pylastfm.constants import (
    LIMIT,
    USER_GETFRIENDS,
    USER_GETINFO,
    USER_GETLOVEDTRACKS,
    USER_GETTOPALBUMS,
    USER_GETTOPARTISTS,
    USER_GETTOPTAGS,
    USER_GETTOPTRACKS,
)

# #########################################################################
# # GET USER FRIENDS
# #########################################################################


def test_get_user_friends(mocker):
    user = 'username'
    return_value = [{'name': 'friend Name'}, {'name': 'friend Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_friends(user=user)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETFRIENDS,
            'user': user,
            'limit': LIMIT,
            'recenttracks': False,
        },
        'friends',
        'friend',
    )
    assert response == return_value


def test_get_user_friends_with_parameters(mocker):
    user = 'username'
    recenttracks = True
    return_value = [{'name': 'friend Name'}, {'name': 'friend Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_friends(user=user, recenttracks=recenttracks)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETFRIENDS,
            'user': user,
            'limit': LIMIT,
            'recenttracks': recenttracks,
        },
        'friends',
        'friend',
    )
    assert response == return_value


#########################################################################
# GET USER INFO
#########################################################################


def test_get_user_info(mocker):
    user = 'username'
    return_value = {'user': {'name': 'User Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_info(user=user)
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETINFO,
        'user': user,
    })
    assert response == return_value['user']


# #########################################################################
# # GET USER LOVED TRACKS
# #########################################################################


def test_get_user_loved_tracks(mocker):
    user = 'username'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_loved_tracks(user=user)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETLOVEDTRACKS,
            'user': user,
            'limit': LIMIT,
        },
        'lovedtracks',
        'track',
    )
    assert response == return_value


# #########################################################################
# # GET USER TOP ALBUMS
# #########################################################################


def test_get_user_top_albums(mocker):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_albums(user=user)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPALBUMS,
            'user': user,
            'period': 'overall',
            'limit': LIMIT,
        },
        'topalbums',
        'album',
    )
    assert response == return_value


def test_get_user_top_albums_with_parameters(mocker):
    user = 'username'
    period = '7day'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_albums(user=user, period=period)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPALBUMS,
            'user': user,
            'period': period,
            'limit': LIMIT,
        },
        'topalbums',
        'album',
    )
    assert response == return_value


# #########################################################################
# # GET USER TOP ARTISTS
# #########################################################################


def test_get_user_top_artists(mocker):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_artists(user=user)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPARTISTS,
            'user': user,
            'period': 'overall',
            'limit': LIMIT,
        },
        'topartists',
        'artist',
    )
    assert response == return_value


def test_get_user_top_artists_with_parameters(mocker):
    user = 'username'
    period = '7day'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_artists(user=user, period=period)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPARTISTS,
            'user': user,
            'period': period,
            'limit': LIMIT,
        },
        'topartists',
        'artist',
    )
    assert response == return_value


# #########################################################################
# # GET USER TOP TRACKS
# #########################################################################


def test_get_user_top_tracks(mocker):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_tracks(user=user)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPTRACKS,
            'user': user,
            'period': 'overall',
            'limit': LIMIT,
        },
        'toptracks',
        'track',
    )
    assert response == return_value


def test_get_user_top_tracks_with_parameters(mocker):
    user = 'username'
    period = '7day'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_tracks(user=user, period=period)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPTRACKS,
            'user': user,
            'period': period,
            'limit': LIMIT,
        },
        'toptracks',
        'track',
    )
    assert response == return_value


# #########################################################################
# # GET USER TOP TAGS
# #########################################################################


def test_get_user_top_tags(mocker):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_tags(user=user)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPTAGS,
            'user': user,
            'limit': LIMIT,
        },
        'toptags',
        'tag',
    )
    assert response == return_value
