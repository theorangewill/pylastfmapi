from typing import Literal

from pylastfm.constants import (
    ALBUM_GETINFO,
    ALBUM_GETTAGS,
    ALBUM_GETTOPTAGS,
    ARTIST_GETINFO,
    ARTIST_GETSIMILAR,
    ARTIST_GETTAGS,
    ARTIST_GETTOPALBUMS,
    ARTIST_GETTOPTAGS,
    ARTIST_GETTOPTRACKS,
    CHART_GETTOPARTISTS,
    CHART_GETTOPTAGS,
    CHART_GETTOPTRACKS,
    TRACK_GETINFO,
    TRACK_GETSIMILAR,
    TRACK_GETTAGS,
    TRACK_GETTOPTAGS,
    USER_GETFRIENDS,
    USER_GETINFO,
    USER_GETLOVEDTRACKS,
    USER_GETTOPALBUMS,
    USER_GETTOPARTISTS,
    USER_GETTOPTAGS,
    USER_GETTOPTRACKS,
)
from pylastfm.exceptions import LastFMException
from pylastfm.request import RequestController
from pylastfm.typehints import ISO639Alpha2Code, T_Period


class LastFM:  # noqa PLR0904
    def __init__(
        self,
        user_agent: str,
        api_key: str,
        api_secret: str = None,
        password_hash: str = None,
        reset_cache: bool = False,
    ) -> None:
        self.user_agent: str = user_agent
        self.api_key: str = api_key
        self.api_secret: str = api_secret
        self.password_hash: str = password_hash
        self.request_controller = RequestController(
            self.user_agent, self.api_key, reset_cache
        )  # , self.api_secret, self.password_hash)

    def get_paginated_data(
        self, payload: dict, parent_key: str, list_key: str, amount: int
    ) -> list[dict]:
        responses = self.request_controller.request_all_pages(
            payload, parent_key, list_key, amount
        )
        response_list = []
        for data in responses:
            response_list.extend(data.json()[parent_key][list_key])
        return response_list

    #########################################################################
    # CHARTS
    #########################################################################

    def get_top_artists(self, amount: int = None) -> list[dict]:
        payload = {'method': CHART_GETTOPARTISTS}
        return self.get_paginated_data(payload, 'artists', 'artist', amount)

    def get_top_tags(self, amount: int = None) -> list[dict]:
        payload = {'method': CHART_GETTOPTAGS}
        return self.get_paginated_data(payload, 'tags', 'tag', amount)

    def get_top_tracks(self, amount: int = None) -> list[dict]:
        payload = {'method': CHART_GETTOPTRACKS}
        return self.get_paginated_data(payload, 'tracks', 'track', amount)

    #########################################################################
    # ALBUMS
    #########################################################################

    def get_album_info(  # noqa PLR0917
        self,
        album: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: Literal[0, 1] = 0,
        lang: ISO639Alpha2Code = 'en',
        username: str = None,
    ) -> dict:
        if not (artist and album) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "album" or "mbid" '
                'for the API'
            )

        payload = {
            'method': ALBUM_GETINFO,
            'artist': artist,
            'album': album,
            'mbid': mbid,
            'autocorrect': autocorrect,
            'lang': lang,
            'username': username,
        }
        return self.request_controller.request(payload).json()['album']

    def get_album_tags(  # noqa PLR0917
        self,
        user: str,
        album: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: Literal[0, 1] = 0,
    ) -> list[dict]:
        if not (artist and album) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "album" or "mbid"'
                ' for the API'
            )
        payload = {
            'method': ALBUM_GETTAGS,
            'user': user,
            'artist': artist,
            'album': album,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.request_controller.request(payload).json()['tags']['tag']

    def get_album_top_tags(  # noqa PLR0917
        self,
        album: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: Literal[0, 1] = 0,
    ) -> list[dict]:
        if not (artist and album) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "album" or "mbid" '
                'for the API'
            )

        payload = {
            'method': ALBUM_GETTOPTAGS,
            'artist': artist,
            'album': album,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.request_controller.request(payload).json()['tags']['tag']

    #########################################################################
    # ARTIST
    #########################################################################

    def get_artist_info(  # noqa PLR0917
        self,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
        lang: str = 'en',
        username: str = None,
    ) -> dict:
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )

        payload = {
            'method': ARTIST_GETINFO,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
            'lang': lang,
            'username': username,
        }
        return self.request_controller.request(payload).json()['artist']

    def get_artist_tags(  # noqa PLR0917
        self,
        user: str,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
    ) -> list[dict]:
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )
        payload = {
            'method': ARTIST_GETTAGS,
            'user': user,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.request_controller.request(payload).json()['tags']['tag']

    def get_artist_top_tags(
        self, artist: str = None, mbid: str = None, autocorrect: int = 0
    ) -> list[dict]:
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )

        payload = {
            'method': ARTIST_GETTOPTAGS,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.request_controller.request(payload).json()['toptags'][
            'tag'
        ]

    def get_artist_top_albums(
        self,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
        amount: int = None,
    ) -> list[dict]:
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )
        payload = {
            'method': ARTIST_GETTOPALBUMS,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.get_paginated_data(payload, 'topalbums', 'album', amount)

    def get_artist_top_tracks(
        self,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
        amount: int = None,
    ) -> list[dict]:
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )

        payload = {
            'method': ARTIST_GETTOPTRACKS,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.get_paginated_data(payload, 'toptracks', 'track', amount)

    def get_artist_similar(
        self,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
        limit: int = 30,
    ) -> dict:
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )

        payload = {
            'method': ARTIST_GETSIMILAR,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
            'limit': limit,
        }
        return self.request_controller.request(payload).json()[
            'similarartists'
        ]['artist']

    #########################################################################
    # TRACK
    #########################################################################

    def get_track_info(
        self,
        track: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
        username: str = None,
    ) -> dict:
        if not (artist and track) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "track" or "mbid" '
                'for the API'
            )

        payload = {
            'method': TRACK_GETINFO,
            'artist': artist,
            'track': track,
            'mbid': mbid,
            'autocorrect': autocorrect,
            'username': username,
        }
        return self.request_controller.request(payload).json()['track']

    def get_track_tags(
        self,
        user: str,
        track: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
    ) -> list[dict]:
        if not (artist and track) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "track" or "mbid"'
                ' for the API'
            )
        payload = {
            'method': TRACK_GETTAGS,
            'user': user,
            'artist': artist,
            'track': track,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.request_controller.request(payload).json()['tags']['tag']

    def get_track_top_tags(
        self,
        track: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
    ) -> list[dict]:
        if not (artist and track) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "track" or "mbid" '
                'for the API'
            )

        payload = {
            'method': TRACK_GETTOPTAGS,
            'artist': artist,
            'track': track,
            'mbid': mbid,
            'autocorrect': autocorrect,
        }
        return self.request_controller.request(payload).json()['toptags'][
            'tag'
        ]

    def get_track_similar(
        self,
        track: str = None,
        artist: str = None,
        mbid: str = None,
        autocorrect: int = 0,
        limit: int = 100,
    ) -> dict:
        if not (artist and track) and not mbid:
            raise LastFMException(
                'You should give the "artist" and "track" or "mbid" '
                'for the API'
            )

        payload = {
            'method': TRACK_GETSIMILAR,
            'track': track,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
            'limit': limit,
        }
        return self.request_controller.request(payload).json()[
            'similartracks'
        ]['track']

    # def search_album(self, album: str) -> list[dict]:
    #     payload = {'method': ALBUM_SEARCH, 'album': album, 'limit': LIMIT}
    #     return self.get_paginated_data(payload, 'results', 'album')

    #########################################################################
    # USER
    #########################################################################

    def get_user_friends(
        self, user: str, recenttracks: bool = False, amount: int = None
    ) -> dict:
        payload = {
            'method': USER_GETFRIENDS,
            'user': user,
            'recenttracks': recenttracks,
        }
        return self.get_paginated_data(payload, 'friends', 'friend', amount)

    def get_user_info(self, user: str) -> dict:
        payload = {'method': USER_GETINFO, 'user': user}
        return self.request_controller.request(payload).json()['user']

    def get_user_loved_tracks(self, user: str, amount: int = None) -> dict:
        payload = {
            'method': USER_GETLOVEDTRACKS,
            'user': user,
        }
        return self.get_paginated_data(payload, 'lovedtracks', 'track', amount)

    # def get_user_personal_tags(  # noqa PLR0917
    #     self,
    #     user: str,
    #     tag: str,
    #     taggingtype: Literal['artist', 'album', 'track']
    # ) -> dict:
    #     payload = {
    #         'method': USER_GETPERSONALTAGS,
    #         'limit': LIMIT,
    #         'user': user,
    #         'tag': tag,
    #         'taggingtype': taggingtype,
    #     }
    # match taggingtype:
    #     case 'artist':
    #     return self.get_paginated_data(payload, 'artists', 'artist')

    def get_user_top_albums(
        self, user: str, period: T_Period = 'overall', amount: int = None
    ) -> dict:
        payload = {
            'method': USER_GETTOPALBUMS,
            'user': user,
            'period': period,
        }
        return self.get_paginated_data(payload, 'topalbums', 'album', amount)

    def get_user_top_artists(
        self, user: str, period: T_Period = 'overall', amount: int = None
    ) -> dict:
        payload = {
            'method': USER_GETTOPARTISTS,
            'user': user,
            'period': period,
        }
        return self.get_paginated_data(payload, 'topartists', 'artist', amount)

    def get_user_top_tracks(
        self, user: str, period: T_Period = 'overall', amount: int = None
    ) -> dict:
        payload = {
            'method': USER_GETTOPTRACKS,
            'user': user,
            'period': period,
        }
        return self.get_paginated_data(payload, 'toptracks', 'track', amount)

    def get_user_top_tags(self, user: str, amount: int = None) -> dict:
        payload = {
            'method': USER_GETTOPTAGS,
            'user': user,
        }
        return self.get_paginated_data(payload, 'toptags', 'tag', amount)
