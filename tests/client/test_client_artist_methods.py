import pytest

from pylastfm.client import LastFM
from pylastfm.constants import (
    ARTIST_GETINFO,
    ARTIST_GETSIMILAR,
    ARTIST_GETTAGS,
    ARTIST_GETTOPALBUMS,
    ARTIST_GETTOPTAGS,
    ARTIST_GETTOPTRACKS,
)
from pylastfm.exceptions import LastFMException

#########################################################################
# GET ARTIST INFO
#########################################################################


def test_get_artist_info(mocker):
    artist = 'artistname'
    return_value = {'artist': {'name': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_info(artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETINFO,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['artist']


def test_get_artist_info_without_artist_name(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_info()


def test_get_artist_info_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_info()


def test_get_artist_info_without_artist_with_mbid(mocker):
    mbid = 'mbidtest'
    return_value = {'artist': {'name': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_info(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETINFO,
        'artist': None,
        'mbid': mbid,
        'autocorrect': 0,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['artist']


def test_get_artist_info_with_parameters(mocker):
    artist = 'artistname'
    autocorrect = 1
    lang = 'pt'
    username = 'usertest'
    return_value = {'artist': {'name': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
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


def test_get_artist_tags(mocker):
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': {'tag': {'name': 'Tag Name'}}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_tags(user=user, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTAGS,
        'user': user,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
    })
    assert response == return_value['tags']['tag']


def test_get_artist_tags_without_artist_name(mocker):
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_tags(user=user)


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


def test_get_artist_tags_without_artist_with_mbid(mocker):
    mbid = 'mbidtest'
    user = 'usertest'
    return_value = {'tags': {'tag': {'name': 'Tag Name'}}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_tags(user=user, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTAGS,
        'user': user,
        'artist': None,
        'mbid': mbid,
        'autocorrect': 0,
    })
    assert response == return_value['tags']['tag']


def test_get_artist_tags_with_parameters(mocker):
    artist = 'artistname'
    user = 'usertest'
    autocorrect = 1
    return_value = {'tags': {'tag': {'name': 'Tag Name'}}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
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


# #########################################################################
# # GET ARTIST TOP TAGS
# #########################################################################


def test_get_artist_top_tags(mocker):
    artist = 'artistname'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_tags(artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTOPTAGS,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
    })
    assert response == return_value['toptags']['tag']


def test_get_artist_top_tags_without_artist_name(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_tags()


def test_get_artist_top_tags_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_tags()


def test_get_artist_top_tags_without_artist_name_with_mbid(mocker):
    mbid = 'mbidtest'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_tags(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETTOPTAGS,
        'artist': None,
        'mbid': mbid,
        'autocorrect': 0,
    })
    assert response == return_value['toptags']['tag']


def test_get_artist_top_tags_with_parameters(mocker):
    artist = 'artistname'
    autocorrect = 1
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
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


def test_get_artist_top_albums(mocker):
    artist = 'artistname'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_albums(artist=artist)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPALBUMS,
            'artist': artist,
            'mbid': None,
            'autocorrect': 0,
        },
        'topalbums',
        'album',
        None,
    )
    assert response == return_value


def test_get_artist_top_albums_without_artist_name(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_albums()


def test_get_artist_top_albums_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_albums()


def test_get_artist_top_albums_without_artist_name_with_mbid(mocker):
    mbid = 'mbidtest'
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_albums(mbid=mbid)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPALBUMS,
            'artist': None,
            'mbid': mbid,
            'autocorrect': 0,
        },
        'topalbums',
        'album',
        None,
    )
    assert response == return_value


def test_get_artist_top_albums_with_parameters(mocker):
    artist = 'artistname'
    autocorrect = 1
    amount = 10
    return_value = [{'name': 'Album Name'}, {'name': 'Album Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_albums(
        artist=artist, autocorrect=autocorrect, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
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


def test_get_artist_top_tracks(mocker):
    artist = 'artistname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_tracks(artist=artist)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPTRACKS,
            'artist': artist,
            'mbid': None,
            'autocorrect': 0,
        },
        'toptracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_artist_top_tracks_without_artist_name(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_tracks()


def test_get_artist_top_tracks_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_top_tracks()


def test_get_artist_top_tracks_without_artist_name_with_mbid(mocker):
    mbid = 'mbidtest'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_tracks(mbid=mbid)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': ARTIST_GETTOPTRACKS,
            'artist': None,
            'mbid': mbid,
            'autocorrect': 0,
        },
        'toptracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_artist_top_tracks_with_parameters(mocker):
    artist = 'artistname'
    amount = 10
    autocorrect = 1
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_top_tracks(
        artist=artist, autocorrect=autocorrect, amount=amount
    )
    ##
    mock_get_paginated_data.assert_called_with(
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


def test_get_artist_similar(mocker):
    artist = 'artistname'
    return_value = {'similarartists': {'artist': [{'name': 'Artist Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_similar(artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETSIMILAR,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
        'limit': 30,
    })
    assert response == return_value['similarartists']['artist']


def test_get_artist_similar_without_artist_name(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_similar()


def test_get_artist_similar_without_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" or "mbid" for the API',
    ):
        _ = client.get_artist_similar()


def test_get_artist_similar_without_artist_name_with_mbid(mocker):
    mbid = 'mbidtest'
    return_value = {'similarartists': {'artist': [{'name': 'Artist Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_similar(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETSIMILAR,
        'artist': None,
        'mbid': mbid,
        'autocorrect': 0,
        'limit': 30,
    })
    assert response == return_value['similarartists']['artist']


def test_get_artist_similar_with_parameters(mocker):
    artist = 'artistname'
    autocorrect = 1
    limit = 10
    return_value = {'similarartists': {'artist': [{'name': 'Artist Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_artist_similar(
        artist=artist, autocorrect=autocorrect, limit=limit
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ARTIST_GETSIMILAR,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'limit': limit,
    })
    assert response == return_value['similarartists']['artist']
