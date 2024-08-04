from pylastfm.client import LastFM
from pylastfm.constants import (
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
            'recenttracks': False,
        },
        'friends',
        'friend',
        None,
    )
    assert response == return_value


def test_get_user_friends_with_parameters(mocker):
    user = 'username'
    recenttracks = True
    amount = 10
    return_value = [{'name': 'friend Name'}, {'name': 'friend Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_friends(
        user=user, recenttracks=recenttracks, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETFRIENDS,
            'user': user,
            'recenttracks': recenttracks,
        },
        'friends',
        'friend',
        amount,
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
        },
        'lovedtracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_user_loved_tracks_with_parameters(mocker):
    user = 'username'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_loved_tracks(user=user, amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETLOVEDTRACKS,
            'user': user,
        },
        'lovedtracks',
        'track',
        amount,
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
        },
        'topalbums',
        'album',
        None,
    )
    assert response == return_value


def test_get_user_top_albums_with_parameters(mocker):
    user = 'username'
    period = '7day'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_albums(
        user=user, period=period, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPALBUMS,
            'user': user,
            'period': period,
        },
        'topalbums',
        'album',
        amount,
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
        },
        'topartists',
        'artist',
        None,
    )
    assert response == return_value


def test_get_user_top_artists_with_parameters(mocker):
    user = 'username'
    period = '7day'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_artists(
        user=user, period=period, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPARTISTS,
            'user': user,
            'period': period,
        },
        'topartists',
        'artist',
        amount,
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
        },
        'toptracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_user_top_tracks_with_parameters(mocker):
    user = 'username'
    period = '7day'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_tracks(
        user=user, period=period, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPTRACKS,
            'user': user,
            'period': period,
        },
        'toptracks',
        'track',
        amount,
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
        },
        'toptags',
        'tag',
        None,
    )
    assert response == return_value


def test_get_user_top_tags_with_parameters(mocker):
    user = 'username'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_user_top_tags(user=user, amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': USER_GETTOPTAGS,
            'user': user,
        },
        'toptags',
        'tag',
        amount,
    )
    assert response == return_value
