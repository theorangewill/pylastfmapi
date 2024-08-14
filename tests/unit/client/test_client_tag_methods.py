from pylastfmapi.constants import (
    TAG_GETINFO,
    TAG_GETSIMILAR,
    TAG_GETTOPALBUMS,
    TAG_GETTOPARTISTS,
    TAG_GETTOPTRACKS,
)

#########################################################################
# GET TAG INFO
#########################################################################


def test_get_tag_info(setup_request_mock):
    tag = 'tagname'
    return_value = {'tag': {'name': 'Tag Name'}}

    client, mock_request_controller = setup_request_mock(return_value)
    ##
    response = client.get_tag_info(tag=tag)
    ##
    mock_request_controller.request.assert_called_with({
        'method': TAG_GETINFO,
        'tag': tag,
        'lang': 'en',
    })
    assert response == return_value['tag']


def test_get_tag_info_with_parameters(setup_request_mock):
    tag = 'tagname'
    lang = 'pt'
    return_value = {'tag': {'name': 'Tag Name'}}

    client, mock_request_controller = setup_request_mock(return_value)
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


def test_get_tag_similar(setup_request_mock):
    tag = 'tagname'
    return_value = {'similartags': {'tag': [{'name': 'Tag Name'}]}}

    client, mock_request_controller = setup_request_mock(return_value)
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


def test_get_tag_top_albums(setup_paginated_mock):
    tag = 'tagname'
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_tag_top_albums(tag=tag)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPALBUMS,
            'tag': tag,
        },
        'albums',
        'album',
        None,
    )
    assert response == return_value


def test_get_tag_top_albums_with_parameters(setup_paginated_mock):
    tag = 'tagname'
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_tag_top_albums(tag=tag, amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_tag_top_artists(setup_paginated_mock):
    tag = 'tagname'
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_tag_top_artists(tag=tag)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPARTISTS,
            'tag': tag,
        },
        'topartists',
        'artist',
        None,
    )
    assert response == return_value


def test_get_tag_top_artists_with_parameters(setup_paginated_mock):
    tag = 'tagname'
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_tag_top_artists(tag=tag, amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
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


def test_get_tag_top_tracks(setup_paginated_mock):
    tag = 'tagname'
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_tag_top_tracks(tag=tag)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPTRACKS,
            'tag': tag,
        },
        'tracks',
        'track',
        None,
    )
    assert response == return_value


def test_get_tag_top_tracks_with_parameters(setup_paginated_mock):
    tag = 'tagname'
    amount = 10
    return_value = [{'name': 'Tag Name'}, {'name': 'Tag Name'}]

    client, mock_request_controller = setup_paginated_mock(return_value)
    ##
    response = client.get_tag_top_tracks(tag=tag, amount=amount)
    ##
    mock_request_controller.get_paginated_data.assert_called_with(
        {
            'method': TAG_GETTOPTRACKS,
            'tag': tag,
        },
        'tracks',
        'track',
        amount,
    )
    assert response == return_value
