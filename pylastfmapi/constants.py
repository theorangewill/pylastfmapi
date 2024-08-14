URL = 'https://ws.audioscrobbler.com/2.0/'
"""
Base URL for the LastFM API
"""

LIMIT = 500
"""
The maximum number of items to retrieve in a single pagination request.
This limit is used to control the amount of data returned by the API.
This can be changed during runtime by the 'amount' parameter in each method
that uses pagination request.
"""

LIMIT_SEARCH = 50
"""
The maximum number of items to retrieve in a single search request.
This limit is used to control the amount of data returned by the API.
This can be changed during runtime by the 'amount' parameter in each method
that uses search request.
"""

MAX_WEEKLY_CHART = 1000
"""
This is set in LastFM backend for the weekly data from users.
"""

#############################################################################
ALBUM_GETINFO = 'album.getInfo'
ALBUM_GETTAGS = 'album.getTags'
ALBUM_GETTOPTAGS = 'album.getTopTags'
ALBUM_SEARCH = 'album.search'

#############################################################################

ARTIST_GETCORRECTION = 'artist.getCorrection'
ARTIST_GETINFO = 'artist.getInfo'
ARTIST_GETSIMILAR = 'artist.getSimilar'
ARTIST_GETTAGS = 'artist.getTags'
ARTIST_GETTOPALBUMS = 'artist.getTopAlbums'
ARTIST_GETTOPTAGS = 'artist.getTopTags'
ARTIST_GETTOPTRACKS = 'artist.getTopTracks'
ARTIST_SEARCH = 'artist.search'

#############################################################################

CHART_GETTOPARTISTS = 'chart.getTopArtists'
CHART_GETTOPTAGS = 'chart.getTopTags'
CHART_GETTOPTRACKS = 'chart.getTopTracks'

#############################################################################

GEO_GETTOPARTISTS = 'geo.getTOPArtists'
GEO_GETOPTRACKS = 'geo.getTOPTracks'

#############################################################################

TAG_GETINFO = 'tag.getInfo'
TAG_GETSIMILAR = 'tag.getSimilar'
TAG_GETTOPALBUMS = 'tag.getTopAlbums'
TAG_GETTOPARTISTS = 'tag.getTopArtists'
TAG_GETTOPTAGS = 'tag.getTopTags'
TAG_GETTOPTRACKS = 'tag.getTopTracks'

#############################################################################

TRACK_GETCORRECTION = 'track.getCorrection'
TRACK_GETINFO = 'track.getInfo'
TRACK_GETSIMILAR = 'track.getSimilar'
TRACK_GETTAGS = 'track.getTags'
TRACK_GETTOPTAGS = 'track.getTopTags'
TRACK_SEARCH = 'track.search'

#############################################################################

LIBRARY_GETARTISTS = 'library.getArtists'
USER_GETFRIENDS = 'user.getFriends'
USER_GETINFO = 'user.getInfo'
USER_GETLOVEDTRACKS = 'user.getLovedTracks'
USER_GETPERSONALTAGS = 'user.getPersonalTags'
USER_GETRECENTTRACKS = 'user.getRecentTracks'
USER_GETTOPALBUMS = 'user.getTopAlbums'
USER_GETTOPARTISTS = 'user.getTopArtists'
USER_GETTOPTAGS = 'user.getTopTags'
USER_GETTOPTRACKS = 'user.getTopTracks'
USER_GETWEEKLYALBUMCHART = 'user.getWeeklyAlbumChart'
USER_GETWEEKLYARTISTCHART = 'user.getWeeklyArtistChart'
USER_GETWEEKLYTRACKCHART = 'user.getWeeklyTrackChart'
