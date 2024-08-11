from datetime import datetime

import pytest

from pylastfm.client import LastFM
from pylastfm.constants import (
    LIBRARY_GETARTISTS,
    MAX_WEEKLY_CHART,
    USER_GETFRIENDS,
    USER_GETINFO,
    USER_GETLOVEDTRACKS,
    USER_GETPERSONALTAGS,
    USER_GETRECENTTRACKS,
    USER_GETTOPALBUMS,
    USER_GETTOPARTISTS,
    USER_GETTOPTAGS,
    USER_GETTOPTRACKS,
    USER_GETWEEKLYALBUMCHART,
    USER_GETWEEKLYARTISTCHART,
    USER_GETWEEKLYTRACKCHART,
)
from pylastfm.exceptions import LastFMException

# #########################################################################
# # GET USER FRIENDS
# #########################################################################


def test_get_user_friends(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'friend Name'}, {'name': 'friend Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_friends(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETFRIENDS,
            'user': user,
            'recenttracks': False,
        },
        'friends',
        'user',
        None,
    )
    assert response == return_value


def test_get_user_friends_with_parameters(setup_paginated_mock):
    user = 'username'
    recenttracks = True
    amount = 10
    return_value = [{'name': 'friend Name'}, {'name': 'friend Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_friends(
        user=user, recenttracks=recenttracks, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETFRIENDS,
            'user': user,
            'recenttracks': recenttracks,
        },
        'friends',
        'user',
        amount,
    )
    assert response == return_value


#########################################################################
# GET USER INFO
#########################################################################


def test_get_user_info(setup_request_mock):
    user = 'username'
    return_value = {'user': {'name': 'User Name'}}

    client, mock_request_controller = setup_request_mock(return_value)
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


def test_get_user_loved_tracks(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_loved_tracks(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETLOVEDTRACKS,
            'user': user,
        },
        'lovedtracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_user_loved_tracks_with_parameters(setup_paginated_mock):
    user = 'username'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_loved_tracks(user=user, amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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
# # GET CHART ARTISTS
# #########################################################################


def test_get_user_library_artists(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_library_artists(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': LIBRARY_GETARTISTS, 'user': user}, 'artists', 'artist', None
    )
    assert response == return_value


def test_get_user_library_artists_with_parameters(setup_paginated_mock):
    user = 'username'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_library_artists(user=user, amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {'method': LIBRARY_GETARTISTS, 'user': user},
        'artists',
        'artist',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET USER PERSONAL TAGS
# #########################################################################


def test_get_user_personal_tags_type_artist(setup_paginated_mock):
    user = 'username'
    tag = 'tagname'
    taggingtype = 'artist'
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype=taggingtype
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        },
        'artists',
        'artist',
        None,
    )
    assert response == return_value


def test_get_user_personal_tags_type_artist_with_parameters(
    setup_paginated_mock,
):
    user = 'username'
    tag = 'tagname'
    taggingtype = 'artist'
    amount = 10
    return_value = [{'name': 'Artist Name'}, {'name': 'Artist Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype=taggingtype, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        },
        'artists',
        'artist',
        amount,
    )
    assert response == return_value


def test_get_user_personal_tags_type_album(setup_paginated_mock):
    user = 'username'
    tag = 'tagname'
    taggingtype = 'album'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype=taggingtype
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        },
        'albums',
        'album',
        None,
    )
    assert response == return_value


def test_get_user_personal_tags_type_album_with_parameters(
    setup_paginated_mock,
):
    user = 'username'
    tag = 'tagname'
    taggingtype = 'album'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype=taggingtype, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        },
        'albums',
        'album',
        amount,
    )
    assert response == return_value


def test_get_user_personal_tags_type_track(setup_paginated_mock):
    user = 'username'
    tag = 'tagname'
    taggingtype = 'track'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype=taggingtype
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        },
        'tracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_user_personal_tags_type_track_with_parameters(
    setup_paginated_mock,
):
    user = 'username'
    tag = 'tagname'
    taggingtype = 'track'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype=taggingtype, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        },
        'tracks',
        'track',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET USER TOP ALBUMS
# #########################################################################


def test_get_user_top_albums(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_top_albums(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_user_top_albums_with_parameters(setup_paginated_mock):
    user = 'username'
    period = '7day'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_top_albums(
        user=user, period=period, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_user_top_artists(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_top_artists(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_user_top_artists_with_parameters(setup_paginated_mock):
    user = 'username'
    period = '7day'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_top_artists(
        user=user, period=period, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_user_top_tracks(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_top_tracks(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_user_top_tracks_with_parameters(setup_paginated_mock):
    user = 'username'
    period = '7day'
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_top_tracks(
        user=user, period=period, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_user_top_tags(setup_request_mock):
    user = 'username'
    return_value = {
        'toptags': {'tag': [{'name': 'Album Name'}, {'name': 'Album Name'}]}
    }

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_top_tags(user=user)
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETTOPTAGS,
        'user': user,
        'limit': None,
    })
    assert response == return_value['toptags']['tag']


def test_get_user_top_tags_with_parameters(setup_request_mock):
    user = 'username'
    amount = 10
    return_value = {
        'toptags': {'tag': [{'name': 'Album Name'}, {'name': 'Album Name'}]}
    }

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_top_tags(user=user, amount=amount)
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETTOPTAGS,
        'user': user,
        'limit': amount,
    })
    assert response == return_value['toptags']['tag']


#########################################################################
# GET USER WEEKLY ALBUM CHART
#########################################################################


def test_get_user_weekly_album_chart(setup_request_mock):
    user = 'username'
    return_value = {
        'weeklyalbumchart': {
            'album': [{'name': 'Album Name'}, {'name': 'Album Name'}]
        }
    }

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_weekly_album_chart(user=user)
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETWEEKLYALBUMCHART,
        'user': user,
        'limit': None,
        'from': None,
        'to': None,
    })
    assert response == return_value['weeklyalbumchart']['album']


def test_get_user_weekly_album_chart_with_parameters(
    mocker, setup_request_mock
):
    user = 'username'
    amount = 10
    date_from = '2024-08-02'
    date_to = '2024-08-07'
    return_value = {
        'weeklyalbumchart': {
            'album': [{'name': 'Album Name'}, {'name': 'Album Name'}]
        }
    }
    mocker.patch(
        'pylastfm.utils.get_timestamp',
        return_value=[
            int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
            int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
        ],
    )

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_weekly_album_chart(
        user=user, amount=amount, date_from=date_from, date_to=date_to
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETWEEKLYALBUMCHART,
        'user': user,
        'limit': amount,
        'from': int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
        'to': int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
    })
    assert response == return_value['weeklyalbumchart']['album']


def test_get_user_weekly_album_chart_with_amount_higher_than_maximum(mocker):
    user = 'username'
    amount = MAX_WEEKLY_CHART + 1
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='For this request, the maximum "amount" is 1000',
    ):
        _ = client.get_user_weekly_album_chart(user=user, amount=amount)


#########################################################################
# GET USER WEEKLY ARTIST CHART
#########################################################################


def test_get_user_weekly_artist_chart(setup_request_mock):
    user = 'username'
    return_value = {
        'weeklyartistchart': {
            'artist': [{'name': 'Artist Name'}, {'name': 'Artist Name'}]
        }
    }

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_weekly_artist_chart(user=user)
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETWEEKLYARTISTCHART,
        'user': user,
        'limit': None,
        'from': None,
        'to': None,
    })
    assert response == return_value['weeklyartistchart']['artist']


def test_get_user_weekly_artist_chart_with_parameters(
    mocker, setup_request_mock
):
    user = 'username'
    amount = 10
    date_from = '2024-08-02'
    date_to = '2024-08-07'
    return_value = {
        'weeklyartistchart': {
            'artist': [{'name': 'Artist Name'}, {'name': 'Artist Name'}]
        }
    }
    mocker.patch(
        'pylastfm.utils.get_timestamp',
        return_value=[
            int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
            int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
        ],
    )

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_weekly_artist_chart(
        user=user, amount=amount, date_from=date_from, date_to=date_to
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETWEEKLYARTISTCHART,
        'user': user,
        'limit': amount,
        'from': int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
        'to': int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
    })
    assert response == return_value['weeklyartistchart']['artist']


def test_get_user_weekly_artist_chart_with_amount_higher_than_maximum(mocker):
    user = 'username'
    amount = MAX_WEEKLY_CHART + 1
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='For this request, the maximum "amount" is 1000',
    ):
        _ = client.get_user_weekly_artist_chart(user=user, amount=amount)


#########################################################################
# GET USER WEEKLY TRACK CHART
#########################################################################


def test_get_user_weekly_track_chart(setup_request_mock):
    user = 'username'
    return_value = {
        'weeklytrackchart': {
            'track': [{'name': 'Track Name'}, {'name': 'Track Name'}]
        }
    }

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_weekly_track_chart(user=user)
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETWEEKLYTRACKCHART,
        'user': user,
        'limit': None,
        'from': None,
        'to': None,
    })
    assert response == return_value['weeklytrackchart']['track']


def test_get_user_weekly_track_chart_with_parameters(
    mocker, setup_request_mock
):
    user = 'username'
    amount = 10
    date_from = '2024-08-02'
    date_to = '2024-08-07'
    return_value = {
        'weeklytrackchart': {
            'track': [{'name': 'Track Name'}, {'name': 'Track Name'}]
        }
    }
    mocker.patch(
        'pylastfm.utils.get_timestamp',
        return_value=[
            int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
            int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
        ],
    )

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_user_weekly_track_chart(
        user=user, amount=amount, date_from=date_from, date_to=date_to
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': USER_GETWEEKLYTRACKCHART,
        'user': user,
        'limit': amount,
        'from': int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
        'to': int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
    })
    assert response == return_value['weeklytrackchart']['track']


def test_get_user_weekly_track_chart_with_amount_higher_than_maximum(mocker):
    user = 'username'
    amount = MAX_WEEKLY_CHART + 1
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='For this request, the maximum "amount" is 1000',
    ):
        _ = client.get_user_weekly_track_chart(user=user, amount=amount)


#########################################################################
# GET USER RECENT TRACKS
#########################################################################


def test_get_user_recent_tracks(setup_paginated_mock):
    user = 'username'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_recent_tracks(user=user)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETRECENTTRACKS,
            'user': user,
            'from': None,
            'to': None,
            'extended': False,
        },
        'recenttracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_user_recent_tracks_with_parameters(mocker, setup_paginated_mock):
    user = 'username'
    date_from = '2023-04-10'
    date_to = '2023-04-12'
    extended = True
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mocker.patch(
        'pylastfm.utils.get_timestamp',
        return_value=[
            int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
            int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
        ],
    )
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_user_recent_tracks(
        user=user,
        amount=amount,
        date_from=date_from,
        date_to=date_to,
        extended=extended,
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': USER_GETRECENTTRACKS,
            'user': user,
            'from': int(datetime.strptime(date_from, '%Y-%m-%d').timestamp()),
            'to': int(datetime.strptime(date_to, '%Y-%m-%d').timestamp()),
            'extended': extended,
        },
        'recenttracks',
        'track',
        amount,
    )
    assert response == return_value
