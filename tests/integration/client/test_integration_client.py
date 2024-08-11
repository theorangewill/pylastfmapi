import pytest

from pylastfm.client import LastFM
from pylastfm.settings import Settings


@pytest.fixture
def client():
    settings = Settings()
    return LastFM(user_agent=settings.USER_AGENT, api_key=settings.API_KEY)


def test_get_top_artists(client):
    amount = 10
    ##
    response = client.get_top_artists(amount=amount)
    ##
    assert len(response) == amount
    assert type(response) is list


def test_get_top_tags(client):
    amount = 15
    ##
    response = client.get_top_tags(amount=amount)
    ##
    assert len(response) == amount
    assert type(response) is list


def test_get_top_tracks(client):
    amount = 13
    ##
    response = client.get_top_tracks(amount=amount)
    ##
    assert len(response) == amount
    assert type(response) is list


def test_get_album_info(client):
    album = 'Plastic Hearts'
    artist = 'Miley Cyrus'
    ##
    response = client.get_album_info(album=album, artist=artist)
    ##
    assert type(response) is dict
    assert response['artist'] == artist
    assert response['name'] == album


def test_get_album_tags(client):
    user = 'theorangewill'
    album = 'Plastic Hearts'
    artist = 'Miley Cyrus'
    ##
    response = client.get_album_tags(user=user, album=album, artist=artist)
    ##
    assert type(response) is list
    if response:
        assert 'name' in response[0]


def test_get_album_top_tags(client):
    album = 'Plastic Hearts'
    artist = 'Miley Cyrus'
    ##
    response = client.get_album_top_tags(album=album, artist=artist)
    ##
    assert type(response) is list
    assert len(response) != 0


def test_search_album(client):
    album = 'Plastic Hearts'
    amount = 5
    ##
    response = client.search_album(album=album, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_artist_info(client):
    artist = 'Miley Cyrus'
    ##
    response = client.get_artist_info(artist=artist)
    ##
    assert type(response) is dict
    assert response['name'] == artist


def test_get_artist_tags(client):
    user = 'theorangewill'
    artist = 'Miley Cyrus'
    ##
    response = client.get_artist_tags(user=user, artist=artist)
    ##
    assert type(response) is list
    if response:
        assert 'name' in response[0]


def test_get_artist_top_tags(client):
    artist = 'Miley Cyrus'
    ##
    response = client.get_artist_top_tags(artist=artist)
    ##
    assert type(response) is list
    assert len(response) != 0


def test_get_artist_top_albums(client):
    artist = 'Miley Cyrus'
    amount = 5
    ##
    response = client.get_artist_top_albums(artist=artist, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount
    assert response[0]['artist']['name'] == artist


def test_get_artist_top_tracks(client):
    artist = 'Miley Cyrus'
    amount = 5
    ##
    response = client.get_artist_top_tracks(artist=artist, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount
    assert response[0]['artist']['name'] == artist


def test_get_artist_similar(client):
    artist = 'Miley Cyrus'
    amount = 10
    ##
    response = client.get_artist_similar(artist=artist, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_search_artist(client):
    artist = 'Miley Cyrus'
    amount = 5
    ##
    response = client.search_artist(artist=artist, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount
    assert response[0]['name'] == artist


def test_get_artist_correction(client):
    artist = 'Miley Cyrus'
    ##
    response = client.get_artist_correction(artist=artist)
    ##
    assert type(response) is dict
    assert response['name'] == artist


def test_get_track_info(client):
    artist = 'Miley Cyrus'
    track = 'Flowers'
    ##
    response = client.get_track_info(artist=artist, track=track)
    ##
    assert type(response) is dict
    assert response['name'] == track
    assert response['artist']['name'] == artist


def test_get_track_tags(client):
    user = 'theorangewill'
    artist = 'Miley Cyrus'
    track = 'Flowers'
    ##
    response = client.get_track_tags(user=user, artist=artist, track=track)
    ##
    assert type(response) is list
    if response:
        assert 'name' in response[0]


def test_get_track_top_tags(client):
    artist = 'Miley Cyrus'
    track = 'Flowers'
    ##
    response = client.get_track_top_tags(artist=artist, track=track)
    ##
    assert type(response) is list
    assert len(response) != 0


def test_get_track_similar(client):
    artist = 'Miley Cyrus'
    track = 'Flowers'
    amount = 10
    ##
    response = client.get_track_similar(
        artist=artist, track=track, amount=amount
    )
    ##
    assert type(response) is list
    assert len(response) == amount


def test_search_track(client):
    artist = 'Miley Cyrus'
    track = 'Flowers'
    amount = 5
    ##
    response = client.search_track(artist=artist, track=track, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount
    assert response[0]['name'] == track
    assert response[0]['artist'] == artist


def test_get_track_correction(client):
    artist = 'Miley Cyrus'
    track = 'Flowers'
    ##
    response = client.get_track_correction(artist=artist, track=track)
    ##
    assert type(response) is dict
    assert response['name'] == track
    assert response['artist']['name'] == artist


def test_get_user_friends(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_friends(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_info(client):
    user = 'theorangewill'
    ##
    response = client.get_user_info(user=user)
    ##
    assert type(response) is dict
    assert response['name'] == user


def test_get_user_loved_tracks(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_loved_tracks(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_library_artists(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_library_artists(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_personal_tags(client):
    user = 'theorangewill'
    tag = 'miley'
    amount = 1
    ##
    response = client.get_user_personal_tags(
        user=user, tag=tag, taggingtype='album', amount=amount
    )
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_top_albums(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_top_albums(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_top_artists(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_top_artists(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_top_tracks(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_top_tracks(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_top_tags(client):
    user = 'theorangewill'
    amount = 1
    ##
    response = client.get_user_top_tags(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_weekly_album_chart(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_weekly_album_chart(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_weekly_artist_chart(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_weekly_artist_chart(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_weekly_track_chart(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_weekly_track_chart(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_user_recent_tracks(client):
    user = 'theorangewill'
    amount = 5
    ##
    response = client.get_user_recent_tracks(user=user, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_country_top_artists(client):
    country = 'Brazil'
    amount = 5
    ##
    response = client.get_country_top_artists(country=country, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_country_top_tracks(client):
    country = 'Brazil'
    amount = 5
    ##
    response = client.get_country_top_tracks(country=country, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_tag_info(client):
    tag = 'rock'
    ##
    response = client.get_tag_info(tag=tag)
    ##
    assert type(response) is dict
    assert response['name'] == tag


def test_get_tag_similar(client):
    tag = 'rock'
    ##
    response = client.get_tag_similar(tag=tag)
    ##
    assert type(response) is list


def test_get_tag_top_albums(client):
    tag = 'rock'
    amount = 5
    ##
    response = client.get_tag_top_albums(tag=tag, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_tag_top_artists(client):
    tag = 'rock'
    amount = 5
    ##
    response = client.get_tag_top_artists(tag=tag, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount


def test_get_tag_top_tracks(client):
    tag = 'rock'
    amount = 5
    ##
    response = client.get_tag_top_tracks(tag=tag, amount=amount)
    ##
    assert type(response) is list
    assert len(response) == amount
