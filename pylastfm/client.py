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
from pylastfm.utils import get_timestamp


class LastFM:  # noqa PLR0904
    """A client for interacting with the LastFM API.

    This class provides methods to access various endpoints of the LastFM API,
    allowing users to retrieve information about albums, artists, charts, tags,
    tracks, and users.
    """

    def __init__(
        self,
        user_agent: str,
        api_key: str,
        api_secret: str | None = None,
        password_hash: str | None = None,
        reset_cache: bool = False,
    ) -> None:
        """Initializes the LastFM client with the necessary
        credentials and settings.

        Args:
            user_agent (str): The user-agent string to be used for API
                requests.
            api_key (str): The API key required for authentication with the
                LastFM API.
            api_secret (str, optional): The API secret for authentication
                (if needed). Defaults to None.
            password_hash (str, optional): A hashed password for authentication
                (if needed). Defaults to None.
            reset_cache (bool, optional): If True, clears the existing cache
                of responses. Defaults to False.
        """
        self.user_agent = user_agent
        self.api_key = api_key
        self.api_secret = api_secret
        self.password_hash = password_hash
        self.request_controller = RequestController(
            self.user_agent, self.api_key, reset_cache
        )

    #########################################################################
    # CHARTS
    #########################################################################

    def get_top_artists(self, amount: int | None = None) -> list[dict]:
        """Fetches the top artists from the LastFM charts.

        This method retrieves the top artists based on the LastFM charts
        and supports pagination to gather a specified amount of data.

        Args:
            amount (int, optional): The total number of artists to retrieve.
                If None, retrieves all available artists. Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing requested data.
        """
        payload = {'method': CHART_GETTOPARTISTS}
        return self.request_controller.get_paginated_data(
            payload, 'artists', 'artist', amount
        )

    def get_top_tags(self, amount: int | None = None) -> list[dict]:
        """Fetches the top tags from the LastFM charts.

        This method retrieves the top tags based on the LastFM charts
        and supports pagination to gather a specified amount of data.

        Args:
            amount (int, optional): The total number of tags to retrieve.
                If None, retrieves all available tags. Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing requested data.
        """
        payload = {'method': CHART_GETTOPTAGS}
        return self.request_controller.get_paginated_data(
            payload, 'tags', 'tag', amount
        )

    def get_top_tracks(self, amount: int | None = None) -> list[dict]:
        """Fetches the top tracks from the LastFM charts.

        This method retrieves the top tracks based on the LastFM charts
        and supports pagination to gather a specified amount of data.

        Args:
            amount (int, optional): The total number of tracks to retrieve.
                If None, retrieves all available tracks. Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing requested data.
        """
        payload = {'method': CHART_GETTOPTRACKS}
        return self.request_controller.get_paginated_data(
            payload, 'tracks', 'track', amount
        )

    #########################################################################
    # ALBUMS
    #########################################################################

    def get_album_info(  # noqa PLR0917
        self,
        album: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        lang: T_ISO639Alpha2Code = 'en',
        username: str | None = None,
    ) -> dict:
        """Fetches information about an album from the LastFM API.

        This method retrieves detailed information about an album,
        such as its artist, title, and other metadata.
        You must provide either the `artist` and `album` or the `mbid` to
        make the request.

        Args:
            album (str, optional): The name of the album. Defaults to None.
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the album.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist or album names. Defaults to False.
            lang (T_ISO639Alpha2Code, optional): The language code for the
                response. Defaults to 'en'.
            username (str, optional): The LastFM username to fetch
                personalized data for. Defaults to None.

        Returns:
            dict: A dictionary containing the album information.

        Raises:
            LastFMException: If neither `artist` and `album` nor `mbid`
                are provided.
        """
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
        album: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
    ) -> list[dict]:
        """Fetches user-assigned tags for an album from the LastFM API.

        This method retrieves the tags a specific user has assigned
        to an album. You must provide either the `artist` and `album` or
        the `mbid` to make the request.

        Args:
            user (str): The LastFM username whose tags are to be retrieved.
            album (str, optional): The name of the album. Defaults to None.
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the album.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects
                misspelled artist or album names. Defaults to False.

        Returns:
            list[dict]: A list of dictionaries containing the user's tags
                for the album.

        Raises:
            LastFMException: If neither `artist` and `album` nor `mbid`
                are provided.
        """
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
        response = self.request_controller.request(payload).json()['tags']
        if 'tag' in response:
            return response['tag']
        else:
            return []

    def get_album_top_tags(  # noqa PLR0917
        self,
        album: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
    ) -> list[dict]:
        """Fetches the top tags for an album from the LastFM API.

        This method retrieves the most popular tags associated with an album,
        based on all users' tagging activity. You must provide either the
        `artist` and `album` or the `mbid` to make the request.

        Args:
            album (str, optional): The name of the album. Defaults to None.
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the album.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist or album names. Defaults to False.

        Returns:
            list[dict]: A list of dictionaries containing the top tags
                for the album.

        Raises:
            LastFMException: If neither `artist` and `album` nor `mbid`
                are provided.
        """
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

        return self.request_controller.request(payload).json()['toptags'][
            'tag'
        ]

    def search_album(
        self, album: str, amount: int | None = None
    ) -> list[dict]:
        """Searches for albums on LastFM matching the given name.

        This method searches the LastFM database for albums that match the
        given album name. It supports pagination to gather a specified amount
        of search results.

        Args:
            album (str): The name of the album to search for.
            amount (int, optional): The total number of results to retrieve.
                If None, retrieves all available results. Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing the search results.
        """
        payload = {'method': ALBUM_SEARCH, 'album': album}
        return self.request_controller.get_search_data(
            payload, 'albummatches', 'album', amount
        )

    #########################################################################
    # ARTIST
    #########################################################################

    def get_artist_info(  # noqa PLR0917
        self,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        lang: str = 'en',
        username: str | None = None,
    ) -> dict:
        """Fetches information about an artist from the LastFM API.

        This method retrieves detailed information about an artist.
        You must provide either the `artist` or the `mbid` to make the request.

        Args:
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the artist.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist names. Defaults to False.
            lang (str, optional): The language code for the response.
                Defaults to 'en'.
            username (str, optional): The LastFM username to fetch
                personalized data for. Defaults to None.

        Returns:
            dict: A dictionary containing the artist information.

        Raises:
            LastFMException: If neither `artist` nor `mbid` is provided.
        """
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
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
    ) -> list[dict]:
        """Fetches user-assigned tags for an artist from the LastFM API.

        This method retrieves the tags a specific user has assigned to
        an artist.
        You must provide either the `artist` or the `mbid` to make the request.

        Args:
            user (str): The LastFM username whose tags are to be retrieved.
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the artist.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist names. Defaults to False.

        Returns:
            list[dict]: A list of dictionaries containing the user's tags for
            the artist.

        Raises:
            LastFMException: If neither `artist` nor `mbid` is provided.
        """
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
        response = self.request_controller.request(payload).json()['tags']
        if 'tag' in response:
            return response['tag']
        else:
            return []

    def get_artist_top_tags(
        self,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
    ) -> list[dict]:
        """Fetches the top tags for an artist from the LastFM API.

        This method retrieves the most popular tags associated with an artist,
        based on all users' tagging activity. You must provide either the
        `artist` or the `mbid` to make the request.

        Args:
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the artist.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist names. Defaults to False.

        Returns:
            list[dict]: A list of dictionaries containing the top tags
            for the artist.

        Raises:
            LastFMException: If neither `artist` nor `mbid` is provided.
        """
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
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches the top albums for an artist from the LastFM API.

        This method retrieves the most popular albums associated with an
        artist.
        You must provide either the `artist` or the `mbid` to make the request.

        Args:
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the artist.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist names. Defaults to False.
            amount (int, optional): The total number of albums to retrieve.
                Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing the artist's
                top albums.

        Raises:
            LastFMException: If neither `artist` nor `mbid` is provided.
        """
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
        return self.request_controller.get_paginated_data(
            payload, 'topalbums', 'album', amount
        )

    def get_artist_top_tracks(
        self,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches the top tracks for an artist from the LastFM API.

        This method retrieves the most popular tracks associated with an
        artist.
        You must provide either the `artist` or the `mbid` to make the request.

        Args:
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the artist.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist names. Defaults to False.
            amount (int, optional): The total number of tracks to retrieve.
                Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing the artist's
                top tracks.

        Raises:
            LastFMException: If neither `artist` nor `mbid` is provided.
        """
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
        return self.request_controller.get_paginated_data(
            payload, 'toptracks', 'track', amount
        )

    def get_artist_similar(
        self,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        amount: int = 30,
    ) -> dict:
        """Fetches similar artists for a given artist from the LastFM API.

        This method retrieves a list of artists similar to the specified
        artist.
        You must provide either the `artist` or the `mbid` to make the request.

        Args:
            artist (str, optional): The name of the artist. Defaults to None.
            mbid (str, optional): The MusicBrainz ID (MBID) of the artist.
                Defaults to None.
            autocorrect (bool, optional): If set to True, corrects misspelled
                artist names. Defaults to False.
            amount (int, optional): The number of similar artists to retrieve.
                Defaults to 30.

        Returns:
            dict: A dictionary containing a list of similar artists.

        Raises:
            LastFMException: If neither `artist` nor `mbid` is provided.
        """
        if not artist and not mbid:
            raise LastFMException(
                'You should give the "artist" or "mbid" for the API'
            )

        payload = {
            'method': ARTIST_GETSIMILAR,
            'artist': artist,
            'mbid': mbid,
            'autocorrect': autocorrect,
            'limit': amount,
        }
        return self.request_controller.request(payload).json()[
            'similarartists'
        ]['artist']

    def search_artist(
        self, artist: str, amount: int | None = None
    ) -> list[dict]:
        """Searches for artists on LastFM that match the given name.

        This method queries the LastFM database for artists that match
        the specified artist name. You can control the number of results
        returned by specifying the `amount` parameter. Results are paginated
        if more results are available.

        Args:
            artist (str): The name of the artist to search for.
            amount (int, optional): The total number of search results
                to retrieve. If None, retrieves all available results.
                Defaults to None.

        Returns:
            list[dict]: A list of dictionaries containing the search results.
                Each dictionary represents an artist.
        """
        payload = {'method': ARTIST_SEARCH, 'artist': artist}
        return self.request_controller.get_search_data(
            payload, 'artistmatches', 'artist', amount
        )

    def get_artist_correction(self, artist: str) -> dict:
        """Checks if the supplied artist name has a correction to a
        canonical artist.

        This method uses the LastFM corrections data to determine if the given
        artist name has a correction that maps it to a canonical artist name.
        It returns a list of possible corrections.

        Args:
            artist (str): The artist name to check for corrections.

        Returns:
            dict: The corrected canonical artist name.
        """
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
        track: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        username: str | None = None,
    ) -> dict:
        """Retrieves detailed information about a track.

        This method fetches detailed information about a track from the
        LastFM API. You need to provide either the artist name and track
        name or the track's MusicBrainz ID (MBID). Optionally,
        you can specify a username to retrieve
        user-specific data and enable autocorrection for potential
        misspellings.

        Args:
            track (str, optional): The name of the track.
                Required if `mbid` is not provided.
            artist (str, optional): The name of the artist.
                Required if `mbid` is not provided.
            mbid (str, optional): The MusicBrainz ID of the track.
                Required if `track` and `artist` are not provided.
            autocorrect (bool, optional): Whether to autocorrect misspellings.
                Defaults to False.
            username (str, optional): The username to retrieve user-specific
                data. Defaults to None.

        Returns:
            dict: A dictionary containing detailed information about the track.

        Raises:
            LastFMException: If neither `track` and `artist` nor `mbid`
                are provided.
        """
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
        track: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
    ) -> list[dict]:
        """Fetches tags assigned to a track by a specific user.

        This method retrieves tags that a user has assigned to a track from
        the LastFM API. You must provide the username and either the track's
        name and artist or the track's MusicBrainz ID (MBID).
        Optionally, you can enable autocorrection for potential misspellings.

        Args:
            user (str): The username who assigned the tags.
            track (str, optional): The name of the track. Required if `mbid`
                is not provided.
            artist (str, optional): The name of the artist. Required if `mbid`
                is not provided.
            mbid (str, optional): The MusicBrainz ID of the track. Required if
                `track` and `artist` are not provided.
            autocorrect (bool, optional): Whether to autocorrect misspellings.
                Defaults to False.

        Returns:
            list[dict]: A list of dictionaries containing tags assigned to
                the track.

        Raises:
            LastFMException: If neither `track` and `artist` nor `mbid`
                are provided.
        """
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
        response = self.request_controller.request(payload).json()['tags']
        if 'tag' in response:
            return response['tag']
        else:
            return []

    def get_track_top_tags(
        self,
        track: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
    ) -> list[dict]:
        """Retrieves the top tags for a track.

        This method fetches the top tags assigned to a track based on user
        tagging from the LastFM API.
        You need to provide either the track name and artist or the track's
        MusicBrainz ID (MBID).
        Optionally, you can enable autocorrection for potential misspellings.

        Args:
            track (str, optional): The name of the track.
                Required if `mbid` is not provided.
            artist (str, optional): The name of the artist.
                Required if `mbid` is not provided.
            mbid (str, optional): The MusicBrainz ID of the track.
                Required if `track` and `artist` are not provided.
            autocorrect (bool, optional): Whether to autocorrect misspellings.
                Defaults to False.

        Returns:
            list[dict]: A list of dictionaries containing the top tags for
                the track.

        Raises:
            LastFMException: If neither `track` and `artist` nor `mbid`
                are provided.
        """
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
        track: str | None = None,
        artist: str | None = None,
        mbid: str | None = None,
        autocorrect: bool = False,
        amount: int = 100,
    ) -> dict:
        """Retrieves a list of tracks similar to the specified track.

        This method fetches a list of tracks similar to the given track
        from the LastFM API.
        You must provide either the track name and artist or the track's
        MusicBrainz ID (MBID).
        Optionally, you can enable autocorrection for misspellings and specify
        the number of similar tracks to retrieve.

        Args:
            track (str, optional): The name of the track.
                Required if `mbid` is not provided.
            artist (str, optional): The name of the artist.
                Required if `mbid` is not provided.
            mbid (str, optional): The MusicBrainz ID of the track.
                Required if `track` and `artist` are not provided.
            autocorrect (bool, optional): Whether to autocorrect misspellings.
                Defaults to False.
            amount (int, optional): The number of similar tracks to retrieve.
                Defaults to 100.

        Returns:
            dict: A dictionary containing similar tracks to the specified
                track.

        Raises:
            LastFMException: If neither `track` and `artist` nor `mbid`
                are provided.

        """
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
            'limit': amount,
        }
        return self.request_controller.request(payload).json()[
            'similartracks'
        ]['track']

    def search_track(
        self, track: str, artist: str | None = None, amount: int | None = None
    ) -> list[dict]:
        """Searches for tracks that match the given track name and artist.

        This method searches for tracks from the LastFM API based on the
        provided track name and optionally artist.
        You can also specify the number of search results to return.

        Args:
            track (str): The name of the track to search for.
            artist (str, optional): The name of the artist. Optional.
            amount (int, optional): The number of search results to return.
                Optional.

        Returns:
            list[dict]: A list of dictionaries containing tracks that match
                the search criteria.
        """
        payload = {'method': TRACK_SEARCH, 'track': track, 'artist': artist}
        return self.request_controller.get_search_data(
            payload, 'trackmatches', 'track', amount
        )

    def get_track_correction(self, track: str, artist: str) -> dict:
        """Uses LastFM corrections data to check whether the supplied track
        has a correction to a canonical track.

        This method queries LastFM's corrections data to determine if the
        given track name has a correction to a canonical track.
        You must provide both the track name and the artist.

        Args:
            track (str): The name of the track to check for corrections.
            artist (str): The name of the artist.

        Returns:
            dict: A dictionary containing detailed information about the track.

        Raises:
            LastFMException: If either `track` or `artist` is not provided.
        """
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
        self, user: str, recenttracks: bool = False, amount: int | None = None
    ) -> list[dict]:
        """Fetches a list of friends for a specific user.

        This method retrieves a list of friends for the given user from the
        LastFM database.
        Supports pagination to handle large result sets and can optionally
        include recent tracks.

        Args:
            user (str): The username of the user whose friends are to be
                retrieved.
            recenttracks (bool, optional): If True, includes recent tracks
                by friends. Defaults to False.
            amount (int, optional): The number of friends to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a friend of the specified user.
        """
        payload = {
            'method': USER_GETFRIENDS,
            'user': user,
            'recenttracks': recenttracks,
        }
        return self.request_controller.get_paginated_data(
            payload, 'friends', 'user', amount
        )

    def get_user_info(self, user: str) -> dict:
        """Fetches detailed information about a specific user.

        This method retrieves detailed information about the given user
            from the LastFM database.

        Args:
            user (str): The username of the user whose information is to
                be retrieved.

        Returns:
            dict: A dictionary containing detailed information about the
                specified user.

        """
        payload = {'method': USER_GETINFO, 'user': user}
        return self.request_controller.request(payload).json()['user']

    def get_user_loved_tracks(
        self, user: str, amount: int | None = None
    ) -> list[dict]:
        """Fetches a list of tracks loved by a specific user.

        This method retrieves a list of tracks that the given user has marked
        as loved from the LastFM database.
        Supports pagination to handle large result sets.

        Args:
            user (str): The username of the user whose loved tracks are to be
                retrieved.
            amount (int, optional): The number of loved tracks to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a loved track of the specified user.
        """
        payload = {
            'method': USER_GETLOVEDTRACKS,
            'user': user,
        }
        return self.request_controller.get_paginated_data(
            payload, 'lovedtracks', 'track', amount
        )

    def get_user_library_artists(
        self, user: str, amount: int | None = None
    ) -> list[dict]:
        """Fetches a list of artists from a user's library.

        This method retrieves a list of artists from the library of the given
        user from the LastFM database.
        Supports pagination to handle large result sets.

        Args:
            user (str): The username of the user whose library artists are to
                be retrieved.
            amount (int, optional): The number of library artists to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about an artist in the user's library.
        """
        payload = {'method': LIBRARY_GETARTISTS, 'user': user}
        return self.request_controller.get_paginated_data(
            payload, 'artists', 'artist', amount
        )

    def get_user_personal_tags(  # noqa PLR0917
        self,
        user: str,
        tag: str,
        taggingtype: Literal['artist', 'album', 'track'],
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches a list of personal tags applied by a user to a specific
        tagging type.

        This method retrieves a list of items (artists, albums, or tracks)
        that the given user has tagged
        with the specified tag. Supports pagination to handle large result
        sets.

        Args:
            user (str): The username of the user whose personal tags are to
                be retrieved.
            tag (str): The tag applied to the items.
            taggingtype (Literal['artist', 'album', 'track']):
                The type of items that are tagged.
            amount (int, optional): The number of tagged items to retrieve.
                f not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about an item tagged by the user.
        """
        payload = {
            'method': USER_GETPERSONALTAGS,
            'user': user,
            'tag': tag,
            'taggingtype': taggingtype,
        }
        match taggingtype:
            case 'artist':
                return self.request_controller.get_paginated_data(
                    payload, 'artists', 'artist', amount
                )
            case 'album':
                return self.request_controller.get_paginated_data(
                    payload, 'albums', 'album', amount
                )
            case 'track':
                return self.request_controller.get_paginated_data(
                    payload, 'tracks', 'track', amount
                )

    def get_user_top_albums(
        self,
        user: str,
        period: T_Period = 'overall',
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches a list of top albums for a specific user.

        This method retrieves a list of the top albums listened to by the
        given user over a specified period.
        Supports pagination to handle large result sets.

        Args:
            user (str): The username of the user whose top albums are to
                be retrieved.
            period (T_Period, optional): The period over which to fetch top
                albums. Defaults to 'overall'.
            amount (int, optional): The number of top albums to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a top album of the specified user.
        """
        payload = {
            'method': USER_GETTOPALBUMS,
            'user': user,
            'period': period,
        }
        return self.request_controller.get_paginated_data(
            payload, 'topalbums', 'album', amount
        )

    def get_user_top_artists(
        self,
        user: str,
        period: T_Period = 'overall',
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches a list of top artists for a specific user.

        This method retrieves a list of the top artists listened to by the
        given user over a specified period.
        Supports pagination to handle large result sets.

        Args:
            user (str): The username of the user whose top artists are to
                be retrieved.
            period (T_Period, optional): The period over which to fetch top
                artists. Defaults to 'overall'.
            amount (int, optional): The number of top artists to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a top artist of the specified user.
        """
        payload = {
            'method': USER_GETTOPARTISTS,
            'user': user,
            'period': period,
        }
        return self.request_controller.get_paginated_data(
            payload, 'topartists', 'artist', amount
        )

    def get_user_top_tracks(
        self,
        user: str,
        period: T_Period = 'overall',
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches a list of top tracks for a specific user.

        This method retrieves a list of the top tracks listened to by the
        given user over a specified period.
        Supports pagination to handle large result sets.

        Args:
            user (str): The username of the user whose top tracks are to
                be retrieved.
            period (T_Period, optional): The period over which to fetch
                top tracks. Defaults to 'overall'.
            amount (int, optional): The number of top tracks to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a top track of the specified user.
        """
        payload = {
            'method': USER_GETTOPTRACKS,
            'user': user,
            'period': period,
        }
        return self.request_controller.get_paginated_data(
            payload, 'toptracks', 'track', amount
        )

    def get_user_top_tags(
        self, user: str, amount: int | None = None
    ) -> list[dict]:
        """Fetches a list of top tags used by a specific user.

        This method retrieves a list of the top tags applied by the given
        user to their items. The tags represent
        the user's most frequently used tags.

        Args:
            user (str): The username of the user whose top tags are to be
                retrieved.
            amount (int, optional): The number of top tags to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a top tag of the specified user.
        """
        payload = {'method': USER_GETTOPTAGS, 'user': user, 'limit': amount}
        return self.request_controller.request(payload).json()['toptags'][
            'tag'
        ]

    def get_user_weekly_album_chart(
        self,
        user: str,
        amount: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict]:
        """Fetches a weekly chart of albums listened to by a specific user.

        This method retrieves a list of albums that the user has listened
        to over a specified week.
        Supports pagination and date filtering.

        Args:
            user (str): The username of the user whose weekly album chart
                is to be retrieved.
            amount (int, optional): The number of albums to retrieve.
                The maximum allowed is 1000.
                If not provided, defaults to all available.
            date_from (str, optional): The start date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            date_to (str, optional): The end date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.

        Returns:
            list[dict]: A list of dictionaries, each containing
                information about an album in the user's weekly chart.

        Raises:
            LastFMException: If `amount` exceeds 1000 or if
                the date range is invalid.
        """
        if amount and amount > MAX_WEEKLY_CHART:
            raise LastFMException(
                f'For this request, the maximum "amount" is {MAX_WEEKLY_CHART}'
            )
        timestamp_from, timestamp_to = get_timestamp(date_from, date_to)

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
        amount: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict]:
        """Fetches a weekly chart of artists listened to by a specific user.

        This method retrieves a list of artists that the user has listened
        to over a specified week.
        Supports pagination and date filtering.

        Args:
            user (str): The username of the user whose weekly artist chart
                is to be retrieved.
            amount (int, optional): The number of artists to retrieve.
                The maximum allowed is 1000.
                If not provided, defaults to all available.
            date_from (str, optional): The start date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            date_to (str, optional): The end date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.

        Returns:
            list[dict]: A list of dictionaries, each containing
                information about an artist in the user's weekly chart.

        Raises:
            LastFMException: If `amount` exceeds 1000
                or if the date range is invalid.
        """
        if amount and amount > MAX_WEEKLY_CHART:
            raise LastFMException(
                f'For this request, the maximum "amount" is {MAX_WEEKLY_CHART}'
            )
        timestamp_from, timestamp_to = get_timestamp(date_from, date_to)

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
        amount: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[dict]:
        """Fetches a weekly chart of tracks listened to by a specific user.

        This method retrieves a list of tracks that the user has listened to
        over a specified week.
        Supports pagination and date filtering.

        Args:
            user (str): The username of the user whose weekly track chart is
                to be retrieved.
            amount (int, optional): The number of tracks to retrieve.
                The maximum allowed is 1000.
                If not provided, defaults to all available.
            date_from (str, optional): The start date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            date_to (str, optional): The end date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.

        Returns:
            list[dict]: A list of dictionaries, each containing
                information about a track in the user's weekly chart.

        Raises:
            LastFMException: If `amount` exceeds 1000 or if the date range
                is invalid.
        """
        if amount and amount > MAX_WEEKLY_CHART:
            raise LastFMException(
                f'For this request, the maximum "amount" is {MAX_WEEKLY_CHART}'
            )
        timestamp_from, timestamp_to = get_timestamp(date_from, date_to)

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
        amount: int | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        extended: bool = False,
    ) -> list[dict]:
        """Fetches the recent tracks listened to by a specific user.

        This method retrieves a list of tracks recently listened to by the
        user. Supports pagination
        and date filtering. If both `date_from` and `date_to` are provided,
        they must be valid dates.

        Args:
            user (str): The username of the user whose recent tracks are to
                be retrieved.
            amount (int, optional): The number of tracks to retrieve.
            date_from (str, optional): The start date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            date_to (str, optional): The end date of the range in
                "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            extended (bool, optional): Whether to include extended data such
                as images. Defaults to False.

        Returns:
            list[dict]: A list of dictionaries, each containing information
                about a track in the user's recent history.

        Raises:
            LastFMException: If `date_from` is greater than or equal to
                `date_to`, or if the date format is invalid.
        """
        timestamp_from, timestamp_to = get_timestamp(date_from, date_to)

        payload = {
            'method': USER_GETRECENTTRACKS,
            'user': user,
            'from': timestamp_from,
            'to': timestamp_to,
            'extended': extended,
        }
        return self.request_controller.get_paginated_data(
            payload, 'recenttracks', 'track', amount
        )

    #########################################################################
    # GEO
    #########################################################################

    def get_country_top_artists(
        self, country: T_ISO3166CountryNames, amount: int | None = None
    ) -> list[dict]:
        """Fetches the top artists for a specified country.

        This method retrieves the top artists in a given country based
        on LastFM data.
        It supports pagination to handle large result sets.

        Args:
            country (T_ISO3166CountryNames): The country code
                (ISO 3166-1 alpha-2) to get top artists for.
            amount (int, optional): The number of top artists to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries containing the top artists
                in the specified country.
        """
        payload = {
            'method': GEO_GETTOPARTISTS,
            'country': country,
        }
        return self.request_controller.get_paginated_data(
            payload, 'topartists', 'artist', amount
        )

    def get_country_top_tracks(
        self,
        country: T_ISO3166CountryNames,
        location: str | None = None,
        amount: int | None = None,
    ) -> list[dict]:
        """Fetches the top tracks for a specified country and optional
        location.

        This method retrieves the top tracks in a given country,
        and optionally, a specific location within that country.
        It supports pagination to handle large result sets.

        Args:
            country (T_ISO3166CountryNames): The country code
                (ISO 3166-1 alpha-2) to get top tracks for.
            location (str, optional): Specific location within the country
                to filter tracks. If not provided, defaults to country-wide
                    data.
            amount (int, optional): The number of top tracks to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries containing the top tracks in
                the specified country and location.
        """
        payload = {
            'method': GEO_GETOPTRACKS,
            'location': location,
            'country': country,
        }
        return self.request_controller.get_paginated_data(
            payload, 'tracks', 'track', amount
        )

    #########################################################################
    # TAG
    #########################################################################

    def get_tag_info(self, tag: str, lang: T_ISO639Alpha2Code = 'en') -> dict:
        """Fetches detailed information about a specific tag.

        This method retrieves detailed information about a given tag from
        the LastFM database.

        Args:
            tag (str): The name of the tag to get information about.
            lang (T_ISO639Alpha2Code, optional):
                The language for the tag information. Defaults to 'en'.

        Returns:
            dict: A dictionary containing information about the specified tag.

        """
        payload = {'method': TAG_GETINFO, 'tag': tag, 'lang': lang}
        return self.request_controller.request(payload).json()['tag']

    def get_tag_similar(
        self,
        tag: str | None = None,
    ) -> list[dict]:
        """Fetches similar tags to the specified tag.

        This method retrieves tags that are similar to the provided tag
        from the LastFM database.

        Args:
            tag (str): The name of the tag to find similar tags for.

        Returns:
            list[dict]: A list of dictionaries containing tags that are
                similar to the specified tag.

        """
        payload = {'method': TAG_GETSIMILAR, 'tag': tag}
        return self.request_controller.request(payload).json()['similartags'][
            'tag'
        ]

    def get_tag_top_albums(
        self, tag: str, amount: int | None = None
    ) -> list[dict]:
        """Fetches the top albums associated with a specific tag.

        This method retrieves a list of top albums associated with the
        provided tag from the LastFM database.
        Supports pagination to handle large result sets.

        Args:
            tag (str): The name of the tag to get top albums for.
            amount (int, optional): The number of top albums to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries containing the top albums
                associated with the specified tag.
        """
        payload = {
            'method': TAG_GETTOPALBUMS,
            'tag': tag,
        }
        return self.request_controller.get_paginated_data(
            payload, 'albums', 'album', amount
        )

    def get_tag_top_artists(
        self, tag: str, amount: int | None = None
    ) -> list[dict]:
        """Fetches the top artists associated with a specific tag.

        This method retrieves a list of top artists associated with the
        provided tag from the LastFM database.
        Supports pagination to handle large result sets.

        Args:
            tag (str): The name of the tag to get top artists for.
            amount (int, optional): The number of top artists to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries containing the top albums
                associated with the specified tag.
        """
        payload = {
            'method': TAG_GETTOPARTISTS,
            'tag': tag,
        }
        return self.request_controller.get_paginated_data(
            payload, 'topartists', 'artist', amount
        )

    def get_tag_top_tracks(
        self, tag: str, amount: int | None = None
    ) -> list[dict]:
        """Fetches the top tracks associated with a specific tag.

        This method retrieves a list of top tracks associated with the
        provided tag from the LastFM database.
        Supports pagination to handle large result sets.

        Args:
            tag (str): The name of the tag to get top tracks for.
            amount (int, optional): The number of top tracks to retrieve.
                If not provided, defaults to all available.

        Returns:
            list[dict]: A list of dictionaries containing the top albums
                associated with the specified tag.
        """
        payload = {
            'method': TAG_GETTOPTRACKS,
            'tag': tag,
        }
        return self.request_controller.get_paginated_data(
            payload, 'tracks', 'track', amount
        )
