import pytest

from pylastfm.client import LastFM
from pylastfm.constants import (
    TRACK_GETCORRECTION,
    TRACK_GETINFO,
    TRACK_GETSIMILAR,
    TRACK_GETTAGS,
    TRACK_GETTOPTAGS,
    TRACK_SEARCH,
)
from pylastfm.exceptions import LastFMException

#########################################################################
# GET TRACK INFO
#########################################################################


def test_get_track_info(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    return_value = {'track': {'name': 'Track Name', 'artist': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_info(track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETINFO,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
        'username': None,
    })
    assert response == return_value['track']


@pytest.mark.parametrize(
    ('artist', 'track', 'mbid'),
    [
        (None, 'trackname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_track_info_missing_parameters(mocker, artist, track, mbid):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_info(track=track, artist=artist, mbid=mbid)


def test_get_track_info_without_track_name_with_mbid(setup_request_mock):
    artist = 'artistname'
    mbid = 'mbidtest'
    return_value = {'track': {'name': 'Track Name', 'artist': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_info(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETINFO,
        'track': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': False,
        'username': None,
    })
    assert response == return_value['track']


def test_get_track_info_with_parameters(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    autocorrect = True
    username = 'usertest'
    return_value = {'track': {'name': 'Track Name', 'artist': 'Artist Name'}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_info(
        track=track,
        artist=artist,
        autocorrect=autocorrect,
        username=username,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETINFO,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'username': username,
    })
    assert response == return_value['track']


#########################################################################
# GET TRACK TAGS
#########################################################################


def test_get_track_tags(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': {'tag': [{'name': 'Tag Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_tags(user=user, track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTAGS,
        'user': user,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['tags']['tag']


@pytest.mark.parametrize(
    ('artist', 'track', 'mbid'),
    [
        (None, 'trackname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_track_tags_missing_parameters(mocker, artist, track, mbid):
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_tags(
            user=user, artist=artist, track=track, mbid=mbid
        )


def test_get_track_tags_without_track_name_with_mbid(setup_request_mock):
    artist = 'artistname'
    mbid = 'mbidtest'
    user = 'usertest'
    return_value = {'tags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_tags(user=user, artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTAGS,
        'user': user,
        'track': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': False,
    })
    assert response == return_value['tags']['tag']


def test_get_track_tags_with_parameters(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    user = 'usertest'
    autocorrect = True
    return_value = {'tags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_tags(
        user=user,
        track=track,
        artist=artist,
        autocorrect=autocorrect,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTAGS,
        'user': user,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
    })
    assert response == return_value['tags']['tag']


def test_get_track_tags_empty_list(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    user = 'usertest'
    return_value = {'tags': []}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_tags(user=user, track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTAGS,
        'user': user,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['tags']


#########################################################################
# GET TRACK TOP TAGS
#########################################################################


def test_get_track_top_tags(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_top_tags(track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTOPTAGS,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
    })
    assert response == return_value['toptags']['tag']


@pytest.mark.parametrize(
    ('artist', 'track', 'mbid'),
    [
        (None, 'trackname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_track_top_tags_missing_parameters(mocker, artist, track, mbid):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_top_tags(track=track, artist=artist, mbid=mbid)


def test_get_track_top_tags_without_track_name_with_mbid(setup_request_mock):
    artist = 'artistname'
    mbid = 'mbidtest'
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_top_tags(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTOPTAGS,
        'track': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': False,
    })
    assert response == return_value['toptags']['tag']


def test_get_track_top_tags_with_parameters(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    autocorrect = True
    return_value = {'toptags': {'tag': {'name': 'Tag Name'}}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_top_tags(
        track=track,
        artist=artist,
        autocorrect=autocorrect,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTOPTAGS,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
    })
    assert response == return_value['toptags']['tag']


# #########################################################################
# # GET TRACK SIMILAR
# #########################################################################


def test_get_track_similar(setup_request_mock):
    artist = 'artistname'
    track = 'trackname'
    return_value = {'similartracks': {'track': [{'name': 'Track Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_similar(track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETSIMILAR,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': False,
        'limit': 100,
    })
    assert response == return_value['similartracks']['track']


@pytest.mark.parametrize(
    ('artist', 'track', 'mbid'),
    [
        (None, 'trackname', None),
        ('artistname', None, None),
        (None, None, None),
    ],
)
def test_get_track_similar_missing_parameters(mocker, artist, track, mbid):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_similar(track=track, artist=artist, mbid=mbid)


def test_get_track_similar_without_artist_name_with_mbid(setup_request_mock):
    mbid = 'mbidtest'
    return_value = {'similartracks': {'track': [{'name': 'Track Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_similar(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETSIMILAR,
        'track': None,
        'artist': None,
        'mbid': mbid,
        'autocorrect': False,
        'limit': 100,
    })
    assert response == return_value['similartracks']['track']


def test_get_track_similar_with_parameters(setup_request_mock):
    artist = 'artistname'
    track = 'trackname'
    autocorrect = True
    amount = 10
    return_value = {'similartracks': {'track': [{'name': 'Track Name'}]}}
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_similar(
        track=track, artist=artist, autocorrect=autocorrect, amount=amount
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETSIMILAR,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'limit': amount,
    })
    assert response == return_value['similartracks']['track']


# #########################################################################
# # SEARCH TRACK
# #########################################################################


def test_search_track(setup_search_mock):
    track = 'trackname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]
    client, mock_request_controller = setup_search_mock(return_value)
    ##
    response = client.search_track(track=track)
    ##
    mock_request_controller.get_search_data.assert_called_with(
        {'method': TRACK_SEARCH, 'track': track, 'artist': None},
        'trackmatches',
        'track',
        None,
    )
    assert response == return_value


def test_search_track_with_parameters(setup_search_mock):
    track = 'trackname'
    artist = 'artistname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]
    client, mock_request_controller = setup_search_mock(return_value)
    ##
    response = client.search_track(track=track, artist=artist, amount=amount)
    ##
    mock_request_controller.get_search_data.assert_called_with(
        {'method': TRACK_SEARCH, 'track': track, 'artist': artist},
        'trackmatches',
        'track',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET TRACK CORRECTION
# #########################################################################


def test_get_track_correction(setup_request_mock):
    track = 'trackname'
    artist = 'artistname'
    return_value = {
        'corrections': {'correction': {'track': {'name': 'Track Name'}}}
    }
    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_track_correction(
        track=track,
        artist=artist,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETCORRECTION,
        'track': track,
        'artist': artist,
    })
    assert response == return_value['corrections']['correction']['track']
