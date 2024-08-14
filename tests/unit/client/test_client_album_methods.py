import pytest

from pylastfmapi.client import LastFM
from pylastfmapi.constants import (
    ALBUM_GETINFO,
    ALBUM_GETTAGS,
    ALBUM_GETTOPTAGS,
    ALBUM_SEARCH,
)
from pylastfmapi.exceptions import LastFMException

#########################################################################
# GET ALBUM INFO
#########################################################################


def test_get_album_info(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    return_value = {'album': {'name': 'Album Name', 'artist': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_info(album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETINFO,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['album']


@pytest.mark.parametrize(
    ('artist', 'album', 'mbid'),
    [
        (None, 'albumname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_album_info_missing_parameters(mocker, artist, album, mbid):
    mocker.patch('pylastfmapi.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_info(artist=artist, album=album, mbid=mbid)


def test_get_album_info_without_album_name_with_mbid(setup_request_mock):
    artist = 'artistname'
    mbid = 'mbidtest'
    return_value = {'album': {'name': 'Album Name', 'artist': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_info(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETINFO,
        'album': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': False,
        'lang': 'en',
        'username': None,
    })
    assert response == return_value['album']


def test_get_album_info_with_parameters(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    autocorrect = True
    lang = 'pt'
    username = 'usertest'
    return_value = {'album': {'name': 'Album Name', 'artist': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
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


def test_get_album_tags(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': {'tag': [{'name': 'Tag Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_tags(user=user, album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTAGS,
        'user': user,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['tags']['tag']


@pytest.mark.parametrize(
    ('artist', 'album', 'mbid'),
    [
        (None, 'albumname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_album_tags_missing_parameters(mocker, artist, album, mbid):
    user = 'usertest'
    mocker.patch('pylastfmapi.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_tags(
            user=user, artist=artist, album=album, mbid=mbid
        )


def test_get_album_tags_without_album_name_with_mbid(setup_request_mock):
    artist = 'artistname'
    mbid = 'mbidtest'
    user = 'usertest'
    return_value = {'tags': {'tag': [{'name': 'Tag Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_tags(user=user, artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTAGS,
        'user': user,
        'album': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': False,
    })
    assert response == return_value['tags']['tag']


def test_get_album_tags_with_parameters(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    user = 'usertest'
    autocorrect = True
    return_value = {'tags': {'tag': [{'name': 'Tag Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
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


def test_get_album_tags_empty_list(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': []}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_tags(user=user, album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTAGS,
        'user': user,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['tags']


#########################################################################
# GET ALBUM TOP TAGS
#########################################################################


def test_get_album_top_tags(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_top_tags(album=album, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTOPTAGS,
        'album': album,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['toptags']['tag']


@pytest.mark.parametrize(
    ('artist', 'album', 'mbid'),
    [
        (None, 'albumname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_album_top_tags_missing_parameters(mocker, artist, album, mbid):
    mocker.patch('pylastfmapi.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "album" or "mbid" for the API',
    ):
        _ = client.get_album_top_tags(artist=artist, album=album, mbid=mbid)


def test_get_album_top_tags_without_album_name_with_mbid(setup_request_mock):
    artist = 'artistname'
    mbid = 'mbidtest'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_album_top_tags(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': ALBUM_GETTOPTAGS,
        'album': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': False,
    })
    assert response == return_value['toptags']['tag']


def test_get_album_top_tags_with_parameters(setup_request_mock):
    album = 'albumname'
    artist = 'artistname'
    autocorrect = True
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
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


def test_search_album(setup_search_mock):
    album = 'albumname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_search_mock(return_value)
    ##
    response = client.search_album(album=album)
    ##
    mock_request_controller.get_search_data.assert_called_with(
        {
            'method': ALBUM_SEARCH,
            'album': album,
        },
        'albummatches',
        'album',
        None,
    )
    assert response == return_value


def test_search_album_with_parameters(setup_search_mock):
    album = 'albumname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    client, mock_request_controller = setup_search_mock(return_value)
    ##
    response = client.search_album(album=album, amount=amount)
    ##
    mock_request_controller.get_search_data.assert_called_with(
        {
            'method': ALBUM_SEARCH,
            'album': album,
        },
        'albummatches',
        'album',
        amount,
    )
    assert response == return_value
