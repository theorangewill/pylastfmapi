from datetime import datetime
from typing import Literal

from pylastfm.constants import (
    ALBUM_GETINFO,
    ALBUM_GETTAGS,
    ALBUM_GETTOPTAGS,
    ALBUM_SEARCH,
    ARTIST_GETCORRECTION,
    ARTIST_GETINFO,
    ARTIST_GETSIMILAR,
    ARTIST_GETTAGS,
    ARTIST_GETTOPALBUMS,
    ARTIST_GETTOPTAGS,
    ARTIST_GETTOPTRACKS,
    ARTIST_SEARCH,
    CHART_GETTOPARTISTS,
    CHART_GETTOPTAGS,
    CHART_GETTOPTRACKS,
    GEO_GETOPTRACKS,
    GEO_GETTOPARTISTS,
    LIBRARY_GETARTISTS,
    LIMIT_SEARCH,
    MAX_WEEKLY_CHART,
    TAG_GETINFO,
    TAG_GETSIMILAR,
    TAG_GETTOPALBUMS,
    TAG_GETTOPARTISTS,
    TAG_GETTOPTRACKS,
    TRACK_GETCORRECTION,
    TRACK_GETINFO,
    TRACK_GETSIMILAR,
    TRACK_GETTAGS,
    TRACK_GETTOPTAGS,
    TRACK_SEARCH,
    USER_GETFRIENDS,
    USER_GETINFO,
    USER_GETLOVEDTRACKS,
    USER_GETPERSONALTAGS,
    USER_GETRECENTTRACKS,
    USER_GETTOPALBUMS,
    USER_GETTOPARTISTS,
    USER_GETTOPTAGS,
    USER_GETTOPTRACKS,
    USER_GETWEEKLYALBUMCHART,
    USER_GETWEEKLYARTISTCHART,
    USER_GETWEEKLYTRACKCHART,
)
from pylastfm.exceptions import LastFMException
from pylastfm.request import RequestController
from pylastfm.typehints import (
    T_ISO639Alpha2Code,
    T_ISO3166CountryNames,
    T_Period,
)


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

    def get_search_data(
        self, payload: dict, parent_key: str, list_key: str, amount: int
    ) -> list[dict]:
        responses = self.request_controller.request_search_pages(
            payload, parent_key, list_key, amount
        )
        response_list = []
        for index, data in enumerate(responses, start=1):
            if index == len(responses):
                left_data = amount % LIMIT_SEARCH
                response_list.extend(
                    data.json()['results'][parent_key][list_key][:left_data]
                )
            else:
                response_list.extend(
                    data.json()['results'][parent_key][list_key]
                )
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
        lang: T_ISO639Alpha2Code = 'en',
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

    def search_album(self, album: str, amount: int = None) -> list[dict]:
        payload = {'method': ALBUM_SEARCH, 'album': album}
        return self.get_search_data(payload, 'albummatches', 'album', amount)

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

    def search_artist(self, artist: str, amount: int = None) -> list[dict]:
        payload = {'method': ARTIST_SEARCH, 'artist': artist}
        return self.get_search_data(payload, 'artistmatches', 'artist', amount)

    def get_artist_correction(self, artist: str) -> list[dict]:
        payload = {
            'method': ARTIST_GETCORRECTION,
            'artist': artist,
        }
        return self.request_controller.request(payload).json()['corrections'][
            'correction'
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

    def search_track(
        self, track: str, artist: str = None, amount: int = None
    ) -> list[dict]:
        payload = {'method': TRACK_SEARCH, 'track': track, 'artist': artist}
        return self.get_search_data(payload, 'trackmatches', 'track', amount)

    def get_track_correction(self, track: str, artist: str) -> list[dict]:
        payload = {
            'method': TRACK_GETCORRECTION,
            'track': track,
            'artist': artist,
        }
        return self.request_controller.request(payload).json()['corrections'][
            'correction'
        ]['track']

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

    def get_user_library_artists(
        self, user: str, amount: int = None
    ) -> list[dict]:
        payload = {'method': LIBRARY_GETARTISTS, 'user': user}
        return self.get_paginated_data(payload, 'artists', 'artist', amount)

    def get_user_personal_tags(  # noqa PLR0917
        self,
        user: str,
        tag: str,
        taggingtype: Literal['artist', 'album', 'track'],
        amount: int = None,
    ) -> dict:
        payload = {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        }
        match taggingtype:
            case 'artist':
                return self.get_paginated_data(
                    payload, 'artists', 'artist', amount
                )
            case 'album':
                return self.get_paginated_data(
                    payload, 'albums', 'album', amount
                )
            case 'track':
                return self.get_paginated_data(
                    payload, 'tracks', 'track', amount
                )

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

    def get_user_weekly_album_chart(
        self,
        user: str,
        amount: int = None,
        date_from: str = None,
        date_to: str = None,
    ) -> dict:
        if amount and amount > MAX_WEEKLY_CHART:
            raise LastFMException(
                'For this request, the maximum "amount" is 1000'
            )
        if date_from and date_to:
            if date_from >= date_to:
                raise LastFMException(
                    'The params "date_from" should be lower than "date_to"'
                )
            try:
                if len(date_from) == len('YYYY-MM-DD'):
                    timestamp_from = int(
                        datetime.strptime(date_from, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_from = int(
                        datetime.strptime(
                            date_from, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
                if len(date_to) == len('YYYY-MM-DD'):
                    timestamp_to = int(
                        datetime.strptime(date_to, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_to = int(
                        datetime.strptime(
                            date_to, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
            except ValueError as e:
                raise LastFMException(
                    'The params "date_from" and "date_to" should be a valid '
                    'date and in "YYYY-MM-DD" or "YYYY-MM-DD %H:%M" format: '
                    f'{e}'
                )
        elif date_from or date_to:
            raise LastFMException(
                'The params "date_from" and "date_to" should be given '
                'together'
            )
        else:
            timestamp_from, timestamp_to = None, None

        payload = {
            'method': USER_GETWEEKLYALBUMCHART,
            'user': user,
            'limit': amount,
            'from': timestamp_from,
            'to': timestamp_to,
        }
        return self.request_controller.request(payload).json()[
            'weeklyalbumchart'
        ]['album']

    def get_user_weekly_artist_chart(
        self,
        user: str,
        amount: int = None,
        date_from: str = None,
        date_to: str = None,
    ) -> dict:
        if amount and amount > MAX_WEEKLY_CHART:
            raise LastFMException(
                'For this request, the maximum "amount" is 1000'
            )
        if date_from and date_to:
            if date_from >= date_to:
                raise LastFMException(
                    'The params "date_from" should be lower than "date_to"'
                )
            try:
                if len(date_from) == len('YYYY-MM-DD'):
                    timestamp_from = int(
                        datetime.strptime(date_from, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_from = int(
                        datetime.strptime(
                            date_from, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
                if len(date_to) == len('YYYY-MM-DD'):
                    timestamp_to = int(
                        datetime.strptime(date_to, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_to = int(
                        datetime.strptime(
                            date_to, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
            except ValueError as e:
                raise LastFMException(
                    'The params "date_from" and "date_to" should be a valid '
                    'date and in "YYYY-MM-DD" or "YYYY-MM-DD %H:%M" format: '
                    f'{e}'
                )
        elif date_from or date_to:
            raise LastFMException(
                'The params "date_from" and "date_to" should be given '
                'together'
            )
        else:
            timestamp_from, timestamp_to = None, None

        payload = {
            'method': USER_GETWEEKLYARTISTCHART,
            'user': user,
            'limit': amount,
            'from': timestamp_from,
            'to': timestamp_to,
        }
        return self.request_controller.request(payload).json()[
            'weeklyartistchart'
        ]['artist']

    def get_user_weekly_track_chart(
        self,
        user: str,
        amount: int = None,
        date_from: str = None,
        date_to: str = None,
    ) -> dict:
        if amount and amount > MAX_WEEKLY_CHART:
            raise LastFMException(
                'For this request, the maximum "amount" is 1000'
            )
        if date_from and date_to:
            if date_from >= date_to:
                raise LastFMException(
                    'The params "date_from" should be lower than "date_to"'
                )
            try:
                if len(date_from) == len('YYYY-MM-DD'):
                    timestamp_from = int(
                        datetime.strptime(date_from, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_from = int(
                        datetime.strptime(
                            date_from, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
                if len(date_to) == len('YYYY-MM-DD'):
                    timestamp_to = int(
                        datetime.strptime(date_to, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_to = int(
                        datetime.strptime(
                            date_to, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
            except ValueError as e:
                raise LastFMException(
                    'The params "date_from" and "date_to" should be a valid '
                    'date and in "YYYY-MM-DD" or "YYYY-MM-DD %H:%M" format: '
                    f'{e}'
                )
        elif date_from or date_to:
            raise LastFMException(
                'The params "date_from" and "date_to" should be given '
                'together'
            )
        else:
            timestamp_from, timestamp_to = None, None

        payload = {
            'method': USER_GETWEEKLYTRACKCHART,
            'user': user,
            'limit': amount,
            'from': timestamp_from,
            'to': timestamp_to,
        }
        return self.request_controller.request(payload).json()[
            'weeklytrackchart'
        ]['track']

    def get_user_recent_tracks(
        self,
        user: str,
        amount: int = None,
        date_from: str = None,
        date_to: str = None,
        extended: bool = False,
    ) -> dict:
        if date_from and date_to:
            if date_from >= date_to:
                raise LastFMException(
                    'The params "date_from" should be lower than "date_to"'
                )
            try:
                if len(date_from) == len('YYYY-MM-DD'):
                    timestamp_from = int(
                        datetime.strptime(date_from, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_from = int(
                        datetime.strptime(
                            date_from, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
                if len(date_to) == len('YYYY-MM-DD'):
                    timestamp_to = int(
                        datetime.strptime(date_to, '%Y-%m-%d').timestamp()
                    )
                else:
                    timestamp_to = int(
                        datetime.strptime(
                            date_to, '%Y-%m-%d %H:%M'
                        ).timestamp()
                    )
            except ValueError as e:
                raise LastFMException(
                    'The params "date_from" and "date_to" should be a valid '
                    'date and in "YYYY-MM-DD" or "YYYY-MM-DD %H:%M" format: '
                    f'{e}'
                )
        elif date_from or date_to:
            raise LastFMException(
                'The params "date_from" and "date_to" should be given '
                'together'
            )
        else:
            timestamp_from, timestamp_to = None, None

        payload = {
            'method': USER_GETRECENTTRACKS,
            'user': user,
            'from': timestamp_from,
            'to': timestamp_to,
            'extended': extended,
        }
        return self.get_paginated_data(
            payload, 'recenttracks', 'track', amount
        )

    #########################################################################
    # GEO
    #########################################################################

    def get_country_top_artists(
        self, country: T_ISO3166CountryNames, amount: int = None
    ) -> dict:
        payload = {
            'method': GEO_GETTOPARTISTS,
            'country': country,
        }
        return self.get_paginated_data(payload, 'topartists', 'artist', amount)

    def get_country_top_tracks(
        self,
        country: T_ISO3166CountryNames,
        location: str = None,
        amount: int = None,
    ) -> dict:
        payload = {
            'method': GEO_GETOPTRACKS,
            'location': location,
            'country': country,
        }
        return self.get_paginated_data(payload, 'tracks', 'track', amount)

    #########################################################################
    # TAG
    #########################################################################

    def get_tag_info(self, tag: str, lang: T_ISO639Alpha2Code = 'en') -> dict:
        payload = {'method': TAG_GETINFO, 'tag': tag, 'lang': lang}
        return self.request_controller.request(payload).json()['tag']

    def get_tag_similar(
        self,
        tag: str = None,
    ) -> dict:
        payload = {'method': TAG_GETSIMILAR, 'tag': tag}
        return self.request_controller.request(payload).json()['similartags'][
            'tag'
        ]

    def get_tag_top_albums(self, tag: str, amount: int = None) -> dict:
        payload = {
            'method': TAG_GETTOPALBUMS,
            'tag': tag,
        }
        return self.get_paginated_data(payload, 'albums', 'album', amount)

    def get_tag_top_artists(self, tag: str, amount: int = None) -> dict:
        payload = {
            'method': TAG_GETTOPARTISTS,
            'tag': tag,
        }
        return self.get_paginated_data(payload, 'topartists', 'artist', amount)

    def get_tag_top_tracks(self, tag: str, amount: int = None) -> dict:
        payload = {
            'method': TAG_GETTOPTRACKS,
            'tag': tag,
        }
        return self.get_paginated_data(payload, 'tracks', 'track', amount)
