from pylastfm.client import LastFM
from pylastfm.constants import (
    TAG_GETINFO,
    TAG_GETSIMILAR,
    TAG_GETTOPALBUMS,
    TAG_GETTOPARTISTS,
    TAG_GETTOPTRACKS,
)

#########################################################################
# GET TAG INFO
#########################################################################


def test_get_tag_info(mocker):
    tag = 'tagname'
    return_value = {'tag': {'name': 'Tag Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_tag_info(tag=tag)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TAG_GETINFO,
        'tag': tag,
        'lang': 'en',
    })
    assert response == return_value['tag']


def test_get_tag_info_with_parameters(mocker):
    tag = 'tagname'
    lang = 'pt'
    return_value = {'tag': {'name': 'Tag Name'}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_tag_info(
        tag=tag,
        lang=lang,
    )
    ##
    mock_request_controller.request.assert_called_with({
        'method': TAG_GETINFO,
        'tag': tag,
        'lang': lang,
    })
    assert response == return_value['tag']


# #########################################################################
# # GET TRACK SIMILAR
# #########################################################################


def test_get_tag_similar(mocker):
    tag = 'tagname'
    return_value = {'similartags': {'tag': [{'name': 'Tag Name'}]}}

    MockRequestController = mocker.patch(
        'pylastfm.client.RequestController', autospec=True
    )
    mock_request_controller = MockRequestController.return_value
    mock_response = mocker.Mock().return_value
    mock_response.json.return_value = return_value
    mock_request_controller.request.return_value = mock_response

    client = LastFM('user_agent_test', 'api_key_test')
    ##
    response = client.get_tag_similar(tag=tag)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TAG_GETSIMILAR,
        'tag': tag,
    })
    assert response == return_value['similartags']['tag']


# #########################################################################
# # GET TAG TOP ALBUMS
# #########################################################################


def test_get_tag_top_albums(mocker):
    tag = 'tagname'
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('tag_agent_test', 'api_key_test')
    ##
    response = client.get_tag_top_albums(tag=tag)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPALBUMS,
            'tag': tag,
        },
        'albums',
        'album',
        None,
    )
    assert response == return_value


def test_get_tag_top_albums_with_parameters(mocker):
    tag = 'tagname'
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('tag_agent_test', 'api_key_test')
    ##
    response = client.get_tag_top_albums(tag=tag, amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPALBUMS,
            'tag': tag,
        },
        'albums',
        'album',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET TAG TOP ARTISTS
# #########################################################################


def test_get_tag_top_artists(mocker):
    tag = 'tagname'
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('tag_agent_test', 'api_key_test')
    ##
    response = client.get_tag_top_artists(tag=tag)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPARTISTS,
            'tag': tag,
        },
        'topartists',
        'artist',
        None,
    )
    assert response == return_value


def test_get_tag_top_artists_with_parameters(mocker):
    tag = 'tagname'
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('tag_agent_test', 'api_key_test')
    ##
    response = client.get_tag_top_artists(tag=tag, amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPARTISTS,
            'tag': tag,
        },
        'topartists',
        'artist',
        amount,
    )
    assert response == return_value


# #########################################################################
# # GET TAG TOP ARTISTS
# #########################################################################


def test_get_tag_top_tracks(mocker):
    tag = 'tagname'
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('tag_agent_test', 'api_key_test')
    ##
    response = client.get_tag_top_tracks(tag=tag)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPTRACKS,
            'tag': tag,
        },
        'tracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_tag_top_tracks_with_parameters(mocker):
    tag = 'tagname'
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    mock_get_paginated_data = mocker.patch.object(
        LastFM,
        'get_paginated_data',
        return_value=return_value,
    )
    client = LastFM('tag_agent_test', 'api_key_test')
    ##
    response = client.get_tag_top_tracks(tag=tag, amount=amount)
    ##
    mock_get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPTRACKS,
            'tag': tag,
        },
        'tracks',
        'track',
        amount,
    )
    assert response == return_value
