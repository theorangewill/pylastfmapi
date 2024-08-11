import pytest

from pylastfm.client import LastFM
from pylastfm.constants import (
    ARTIST_GETCORRECTION,
    ARTIST_GETINFO,
    ARTIST_GETSIMILAR,
    ARTIST_GETTAGS,
    ARTIST_GETTOPALBUMS,
    ARTIST_GETTOPTAGS,
    ARTIST_GETTOPTRACKS,
    ARTIST_SEARCH,
)
from pylastfm.exceptions import LastFMException

#########################################################################
# GET ARTIST INFO
#########################################################################


def test_get_artist_info(setup_request_mock):
    artist = 'artistname'
    return_value = {'artist': {'name': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_info(artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETINFO,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['artist']


def test_get_artist_info_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_info()


def test_get_artist_info_without_artist_with_mbid(setup_request_mock):
    mbid = 'mbidtest'
    return_value = {'artist': {'name': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_info(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETINFO,
        'artist': None,
        'mbid': mbid,
        'autocorrect': False,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['artist']


def test_get_artist_info_with_parameters(setup_request_mock):
    artist = 'artistname'
    autocorrect = True
    lang = 'pt'
    username = 'usertest'
    return_value = {'artist': {'name': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_info(
        artist=artist,
        autocorrect=autocorrect,
        lang=lang,
        username=username,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETINFO,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'lang': lang,
        'username': username,
    })
    assert response == return_value['artist']


#########################################################################
# GET ARTIST TAGS
#########################################################################


def test_get_artist_tags(setup_request_mock):
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': {'tag': [{'name': 'Tag Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_tags(user=user, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTAGS,
        'user': user,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['tags']['tag']


def test_get_artist_tags_without_artist_and_mbid(mocker):
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_tags(user=user)


def test_get_artist_tags_without_artist_with_mbid(setup_request_mock):
    mbid = 'mbidtest'
    user = 'usertest'
    return_value = {'tags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_tags(user=user, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTAGS,
        'user': user,
        'artist': None,
        'mbid': mbid,
        'autocorrect': False,
    })
    assert response == return_value['tags']['tag']


def test_get_artist_tags_with_parameters(setup_request_mock):
    artist = 'artistname'
    user = 'usertest'
    autocorrect = True
    return_value = {'tags': {'tag': [{'name': 'Tag Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_tags(
        user=user,
        artist=artist,
        autocorrect=autocorrect,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTAGS,
        'user': user,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
    })
    assert response == return_value['tags']['tag']


def test_get_artist_tags_empty_list(setup_request_mock):
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': []}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_tags(user=user, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTAGS,
        'user': user,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['tags']


# #########################################################################
# # GET ARTIST TOP TAGS
# #########################################################################


def test_get_artist_top_tags(setup_request_mock):
    artist = 'artistname'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_top_tags(artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTOPTAGS,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['toptags']['tag']


def test_get_artist_top_tags_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_tags()


def test_get_artist_top_tags_without_artist_name_with_mbid(setup_request_mock):
    mbid = 'mbidtest'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_top_tags(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTOPTAGS,
        'artist': None,
        'mbid': mbid,
        'autocorrect': False,
    })
    assert response == return_value['toptags']['tag']


def test_get_artist_top_tags_with_parameters(setup_request_mock):
    artist = 'artistname'
    autocorrect = True
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_top_tags(
        artist=artist,
        autocorrect=autocorrect,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTOPTAGS,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
    })
    assert response == return_value['toptags']['tag']


# #########################################################################
# # GET ARTIST TOP ALBUMS
# #########################################################################


def test_get_artist_top_albums(setup_paginated_mock):
    artist = 'artistname'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_artist_top_albums(artist=artist)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPALBUMS,
            'artist': artist,
            'mbid': None,
            'autocorrect': False,
        },
        'topalbums',
        'album',
        None,
    )
    assert response == return_value


def test_get_artist_top_albums_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_albums()


def test_get_artist_top_albums_without_artist_name_with_mbid(
    setup_paginated_mock,
):
    mbid = 'mbidtest'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_artist_top_albums(mbid=mbid)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPALBUMS,
            'artist': None,
            'mbid': mbid,
            'autocorrect': False,
        },
        'topalbums',
        'album',
        None,
    )
    assert response == return_value


def test_get_artist_top_albums_with_parameters(setup_paginated_mock):
    artist = 'artistname'
    autocorrect = True
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_artist_top_albums(
        artist=artist, autocorrect=autocorrect, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPALBUMS,
            'artist': artist,
            'mbid': None,
            'autocorrect': autocorrect,
        },
        'topalbums',
        'album',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET ARTIST TOP TRACKS
# #########################################################################


def test_get_artist_top_tracks(setup_paginated_mock):
    artist = 'artistname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_artist_top_tracks(artist=artist)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPTRACKS,
            'artist': artist,
            'mbid': None,
            'autocorrect': False,
        },
        'toptracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_artist_top_tracks_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_tracks()


def test_get_artist_top_tracks_without_artist_name_with_mbid(
    setup_paginated_mock,
):
    mbid = 'mbidtest'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_artist_top_tracks(mbid=mbid)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPTRACKS,
            'artist': None,
            'mbid': mbid,
            'autocorrect': False,
        },
        'toptracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_artist_top_tracks_with_parameters(setup_paginated_mock):
    artist = 'artistname'
    amount = 10
    autocorrect = True
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]
    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_artist_top_tracks(
        artist=artist, autocorrect=autocorrect, amount=amount
    )
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPTRACKS,
            'artist': artist,
            'mbid': None,
            'autocorrect': autocorrect,
        },
        'toptracks',
        'track',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET ARTIST SIMILAR
# #########################################################################


def test_get_artist_similar(setup_request_mock):
    artist = 'artistname'
    return_value = {'similarartists': {'artist': [{'name': 'Artist Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_similar(artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETSIMILAR,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
        'limit': 30,
    })
    assert response == return_value['similarartists']['artist']


def test_get_artist_similar_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_similar()


def test_get_artist_similar_without_artist_name_with_mbid(setup_request_mock):
    mbid = 'mbidtest'
    return_value = {'similarartists': {'artist': [{'name': 'Artist Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_similar(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETSIMILAR,
        'artist': None,
        'mbid': mbid,
        'autocorrect': False,
        'limit': 30,
    })
    assert response == return_value['similarartists']['artist']


def test_get_artist_similar_with_parameters(setup_request_mock):
    artist = 'artistname'
    autocorrect = True
    amount = 10
    return_value = {'similarartists': {'artist': [{'name': 'Artist Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_similar(
        artist=artist, autocorrect=autocorrect, amount=amount
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETSIMILAR,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'limit': amount,
    })
    assert response == return_value['similarartists']['artist']


# #########################################################################
# # SEARCH ARTIST
# #########################################################################


def test_search_artist(mocker):
    artist = 'artistname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_request_controller.get_search_data.return_value = return_value
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.search_artist(artist=artist)
    ##
    mock_request_controller.get_search_data.assert_called_with(
        {
            'method': ARTIST_SEARCH,
            'artist': artist,
        },
        'artistmatches',
        'artist',
        None,
    )
    assert response == return_value


def test_search_artist_with_parameters(setup_search_mock):
    artist = 'artistname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_search_mock(return_value)
    ##
    response = client.search_artist(artist=artist, amount=amount)
    ##
    mock_request_controller.get_search_data.assert_called_with(
        {
            'method': ARTIST_SEARCH,
            'artist': artist,
        },
        'artistmatches',
        'artist',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET ARTIST CORRECTION
# #########################################################################


def test_get_artist_correction(setup_request_mock):
    artist = 'artistname'
    return_value = {
        'corrections': {'correction': {'artist': {'name': 'Artist Name'}}}
    }
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_artist_correction(
        artist=artist,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETCORRECTION,
        'artist': artist,
    })
    assert response == return_value['corrections']['correction']['artist']
