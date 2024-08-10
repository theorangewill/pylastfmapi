import pytest

from pylastfm.client import LastFM
from pylastfm.constants import (
    ALBUM_GETINFO,
    ALBUM_GETTAGS,
    ALBUM_GETTOPTAGS,
    ALBUM_SEARCH,
)
from pylastfm.exceptions import LastFMException

#########################################################################
# GET ALBUM INFO
#########################################################################


def test_get_album_info(mocker):
    album = 'albumname'
    artist = 'artistname'
    return_value = {'album': {'name': 'Album Name', 'artist': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_album_info(album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETINFO,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['album']


def test_get_album_info_without_artist_name(mocker):
    album = 'albumname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_info(album=album)


def test_get_album_info_without_album_name(mocker):
    artist = 'artistname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_info(artist=artist)


def test_get_album_info_without_album_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_info()


def test_get_album_info_without_album_name_with_mbid(mocker):
    artist = 'artistname'
    mbid = 'mbidtest'
    return_value = {'album': {'name': 'Album Name', 'artist': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_album_info(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETINFO,
        'album': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': 0,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['album']


def test_get_album_info_with_parameters(mocker):
    album = 'albumname'
    artist = 'artistname'
    autocorrect = 1
    lang = 'pt'
    username = 'usertest'
    return_value = {'album': {'name': 'Album Name', 'artist': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_album_info(
        album=album,
        artist=artist,
        autocorrect=autocorrect,
        lang=lang,
        username=username,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETINFO,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'lang': lang,
        'username': username,
    })
    assert response == return_value['album']


#########################################################################
# GET ALBUM TAGS
#########################################################################


def test_get_album_tags(mocker):
    album = 'albumname'
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
    response = client.get_album_tags(user=user, album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTAGS,
        'user': user,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
    })
    assert response == return_value['tags']['tag']


def test_get_album_tags_without_artist_name(mocker):
    album = 'albumname'
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_tags(user=user, album=album)


def test_get_album_tags_without_album_name(mocker):
    artist = 'artistname'
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_tags(user=user, artist=artist)


def test_get_album_tags_without_album_artist_and_mbid(mocker):
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_tags(user=user)


def test_get_album_tags_without_album_name_with_mbid(mocker):
    artist = 'artistname'
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
    response = client.get_album_tags(user=user, artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTAGS,
        'user': user,
        'album': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': 0,
    })
    assert response == return_value['tags']['tag']


def test_get_album_tags_with_parameters(mocker):
    album = 'albumname'
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
    response = client.get_album_tags(
        user=user,
        album=album,
        artist=artist,
        autocorrect=autocorrect,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTAGS,
        'user': user,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
    })
    assert response == return_value['tags']['tag']


#########################################################################
# GET ALBUM TOP TAGS
#########################################################################


def test_get_album_top_tags(mocker):
    album = 'albumname'
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
    response = client.get_album_top_tags(album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTOPTAGS,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
    })
    assert response == return_value['toptags']['tag']


def test_get_album_top_tags_without_artist_name(mocker):
    album = 'albumname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_top_tags(album=album)


def test_get_album_top_tags_without_album_name(mocker):
    artist = 'artistname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_top_tags(artist=artist)


def test_get_album_top_tags_without_album_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_top_tags()


def test_get_album_top_tags_without_album_name_with_mbid(mocker):
    artist = 'artistname'
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
    response = client.get_album_top_tags(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTOPTAGS,
        'album': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': 0,
    })
    assert response == return_value['toptags']['tag']


def test_get_album_top_tags_with_parameters(mocker):
    album = 'albumname'
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
    response = client.get_album_top_tags(
        album=album,
        artist=artist,
        autocorrect=autocorrect,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTOPTAGS,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
    })
    assert response == return_value['toptags']['tag']


# #########################################################################
# # SEARCH ALBUM
# #########################################################################


def test_search_album(mocker):
    album = 'albumname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_search_data = mocker.patch.object(
        LastFM,
        'get_search_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.search_album(album=album)
    ##
    mock_get_search_data.assert_called_with(
        {
            'method': ALBUM_SEARCH,
            'album': album,
        },
        'albummatches',
        'album',
        None,
    )
    assert response == return_value


def test_search_album_with_parameters(mocker):
    album = 'albumname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_search_data = mocker.patch.object(
        LastFM,
        'get_search_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.search_album(album=album, amount=amount)
    ##
    mock_get_search_data.assert_called_with(
        {
            'method': ALBUM_SEARCH,
            'album': album,
        },
        'albummatches',
        'album',
        amount,
    )
    assert response == return_value
