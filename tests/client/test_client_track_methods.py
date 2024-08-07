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
# GET ARTIST INFO
#########################################################################


def test_get_track_info(mocker):
    track = 'trackname'
    artist = 'artistname'
    return_value = {'track': {'name': 'Track Name', 'artist': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_track_info(track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETINFO,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
        'username': None,
    })
    assert response == return_value['track']


def test_get_track_info_without_artist_name(mocker):
    track = 'trackname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_info(track=track)


def test_get_track_info_without_track_name(mocker):
    artist = 'artistname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_info(artist=artist)


def test_get_track_info_without_track_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_info()


def test_get_track_info_without_track_name_with_mbid(mocker):
    artist = 'artistname'
    mbid = 'mbidtest'
    return_value = {'track': {'name': 'Track Name', 'artist': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_track_info(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETINFO,
        'track': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': 0,
        'username': None,
    })
    assert response == return_value['track']


def test_get_track_info_with_parameters(mocker):
    track = 'trackname'
    artist = 'artistname'
    autocorrect = 1
    username = 'usertest'
    return_value = {'track': {'name': 'Track Name', 'artist': 'Artist Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
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


def test_get_track_tags(mocker):
    track = 'trackname'
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
    response = client.get_track_tags(user=user, track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTAGS,
        'user': user,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
    })
    assert response == return_value['tags']['tag']


def test_get_track_tags_without_artist_name(mocker):
    track = 'trackname'
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_tags(user=user, track=track)


def test_get_track_tags_without_track_name(mocker):
    artist = 'artistname'
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_tags(user=user, artist=artist)


def test_get_track_tags_without_track_artist_and_mbid(mocker):
    user = 'usertest'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_tags(user=user)


def test_get_track_tags_without_track_name_with_mbid(mocker):
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
    response = client.get_track_tags(user=user, artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTAGS,
        'user': user,
        'track': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': 0,
    })
    assert response == return_value['tags']['tag']


def test_get_track_tags_with_parameters(mocker):
    track = 'trackname'
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


#########################################################################
# GET TRACK TOP TAGS
#########################################################################


def test_get_track_top_tags(mocker):
    track = 'trackname'
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
    response = client.get_track_top_tags(track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTOPTAGS,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
    })
    assert response == return_value['toptags']['tag']


def test_get_track_top_tags_without_artist_name(mocker):
    track = 'trackname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_top_tags(track=track)


def test_get_track_top_tags_without_track_name(mocker):
    artist = 'artistname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_top_tags(artist=artist)


def test_get_track_top_tags_without_track_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_top_tags()


def test_get_track_top_tags_without_track_name_with_mbid(mocker):
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
    response = client.get_track_top_tags(artist=artist, mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETTOPTAGS,
        'track': None,
        'artist': artist,
        'mbid': mbid,
        'autocorrect': 0,
    })
    assert response == return_value['toptags']['tag']


def test_get_track_top_tags_with_parameters(mocker):
    track = 'trackname'
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


def test_get_track_similar(mocker):
    artist = 'artistname'
    track = 'trackname'
    return_value = {'similartracks': {'track': [{'name': 'Track Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_track_similar(track=track, artist=artist)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETSIMILAR,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': 0,
        'limit': 100,
    })
    assert response == return_value['similartracks']['track']


def test_get_track_similar_without_artist_name(mocker):
    track = 'trackname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_similar(track=track)


def test_get_track_similar_without_track_name(mocker):
    artist = 'artistname'
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_similar(artist=artist)


def test_get_track_similar_without_track_artist_and_mbid(mocker):
    mocker.patch('pylastfm.client.RequestController')
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    with pytest.raises(
        LastFMException,
        match='You should give the "artist" and "track" or "mbid" for the API',
    ):
        _ = client.get_track_similar()


def test_get_track_similar_without_artist_name_with_mbid(mocker):
    mbid = 'mbidtest'
    return_value = {'similartracks': {'track': [{'name': 'Track Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_track_similar(mbid=mbid)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETSIMILAR,
        'track': None,
        'artist': None,
        'mbid': mbid,
        'autocorrect': 0,
        'limit': 100,
    })
    assert response == return_value['similartracks']['track']


def test_get_track_similar_with_parameters(mocker):
    artist = 'artistname'
    track = 'trackname'
    autocorrect = 1
    limit = 10
    return_value = {'similartracks': {'track': [{'name': 'Track Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_track_similar(
        track=track, artist=artist, autocorrect=autocorrect, limit=limit
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TRACK_GETSIMILAR,
        'track': track,
        'artist': artist,
        'mbid': None,
        'autocorrect': autocorrect,
        'limit': limit,
    })
    assert response == return_value['similartracks']['track']


# #########################################################################
# # SEARCH TRACK
# #########################################################################


def test_search_track(mocker):
    track = 'trackname'
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_search_data = mocker.patch.object(
        LastFM,
        'get_search_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.search_track(track=track)
    ##
    mock_get_search_data.assert_called_with(
        {'method': TRACK_SEARCH, 'track': track, 'artist': None},
        'trackmatches',
        'track',
        None,
    )
    assert response == return_value


def test_search_track_with_parameters(mocker):
    track = 'trackname'
    artist = 'artistname'
    amount = 10
    return_value = [{'name': 'Track Name'}, {'name': 'Track Name'}]

    mock_get_search_data = mocker.patch.object(
        LastFM,
        'get_search_data',
        return_value=return_value,
    )
    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.search_track(track=track, artist=artist, amount=amount)
    ##
    mock_get_search_data.assert_called_with(
        {'method': TRACK_SEARCH, 'track': track, 'artist': artist},
        'trackmatches',
        'track',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET TRACK CORRECTION
# #########################################################################


def test_get_track_correction(mocker):
    track = 'trackname'
    artist = 'artistname'
    return_value = {
        'corrections': {'correction': {'track': {'name': 'Tag Name'}}}
    }

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
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
