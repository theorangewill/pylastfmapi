# Methods

Here we have the list of available methods to fetch data from LastFM API.
The methods are gathered in sections: Album, Artist, Chart, Country, Tag, Track, and User.

To understand the parameters of this package, please go to the specifications [here](api/client.md).

The LastFM API official doc gives the output format, please check [here](https://www.last.fm/api/intro).
However, the community has written another version that could help, check here [here](https://lastfm-docs.github.io/api-docs/).


### Album methods
- **[`get_album_info`](api/client.md#client.LastFM.get_album_info)**: detailed information about a specific album.
- **[`get_album_tags`](api/client.md#client.LastFM.get_album_tags)**: tags associated with a specific album by a specific user.
- **[`get_album_top_tags`](api/client.md#client.LastFM.get_album_top_tags)**: the top tags associated with a specific album by all users.
- **[`search_album`](api/client.md#client.LastFM.search_album)**: fetches all albums from a LastFM database search

### Artists methods
- **[`get_artist_correction`](api/client.md#client.LastFM.get_artist_correction)**: gets a correction to a canonical artist LastFM profile.
- **[`get_artist_info`](api/client.md#client.LastFM.get_artist_info)**: detailed information about an artist.
- **[`get_artist_tags`](api/client.md#client.LastFM.get_artist_tags)**: tags associated with an artist by a specific user.
- **[`get_artist_top_albums`](api/client.md#client.LastFM.get_artist_top_albums)**: the top albums of an artist.
- **[`get_artist_top_tracks`](api/client.md#client.LastFM.get_artist_top_tracks)**: the top tracks of an artist.
- **[`get_artist_top_tags`](api/client.md#client.LastFM.get_artist_top_tags)**: the top tags associated with a specific artist by all users.
- **[`get_artist_similar`](api/client.md#client.LastFM.get_artist_similar)**: artists similar to a specific artist.
- **[`search_artist`](api/client.md#client.LastFM.search_artist)**: fetches all artists from a LastFM database search

### Chart methods
- **[`get_top_artists`](api/client.md#client.LastFM.get_top_artists)**: the top artists from the LastFM charts.
- **[`get_top_tags`](api/client.md#client.LastFM.get_top_tags)**: the top tags from the LastFM charts.
- **[`get_top_tracks`](api/client.md#client.LastFM.get_top_tracks)**: the top tracks from the LastFM charts.

### Country methods
- **[`get_country_top_artists`](api/client.md#client.LastFM.get_country_top_artists)**: the top artists for a specified country.
- **[`get_country_top_tracks`](api/client.md#client.LastFM.get_country_top_tracks)**: the top tracks for a specified country.

### Tag methods
- **[`get_tag_info`](api/client.md#client.LastFM.get_tag_info)**: detailed information about a tag.
- **[`get_tag_similar`](api/client.md#client.LastFM.get_tag_similar)**: tags similar to a specific tag.
- **[`get_tag_top_albums`](api/client.md#client.LastFM.get_tag_top_albums)**: the top albums associated with a specific tag.
- **[`get_tag_top_artists`](api/client.md#client.LastFM.get_tag_top_artists)**: the top artists associated with a specific tag.
- **[`get_tag_top_tracks`](api/client.md#client.LastFM.get_tag_top_tracks)**: the top tracks associated with a specific tag.

### Track methods
- **[`get_track_correction`](api/client.md#client.LastFM.get_track_correction)**: gets a correction to a canonical track LastFM definition.
- **[`get_track_info`](api/client.md#client.LastFM.get_track_info)**: detailed information about a specific track.
- **[`get_track_tags`](api/client.md#client.LastFM.get_track_tags)**: tags associated with a track by a specific user.
- **[`get_track_top_tags`](api/client.md#client.LastFM.get_track_top_tags)**: the top tags associated with a specific track by all users.
- **[`get_track_similar`](api/client.md#client.LastFM.get_track_similar)**: tracks similar to a specific track.
- **[`search_track`](api/client.md#client.LastFM.search_track)**: fetches all tracks from a LastFM database search


### User methods
- **[`get_user_friends`](api/client.md#client.LastFM.get_user_friends)**: the list of friends of a user.
- **[`get_user_info`](api/client.md#client.LastFM.get_user_info)**: detailed information about a user.
- **[`get_user_library_artists`](api/client.md#client.LastFM.get_user_library_artists)**: the list of artists in a user's library
- **[`get_user_loved_tracks`](api/client.md#client.LastFM.get_user_loved_tracks)**: the tracks that a user has marked as loved.
- **[`get_user_personal_tags`](api/client.md#client.LastFM.get_user_personal_tags)**: the personal tags a user has applied to tracks, artists, or albums.
- **[`get_user_recent_tracks`](api/client.md#client.LastFM.get_user_recent_tracks)**: recent tracks a user has listened to.
- **[`get_user_top_albums`](api/client.md#client.LastFM.get_user_top_albums)**: the top albums of a user over a specific range of time (`'overall', '7day', '1month', '3month', '6month', '12month'`).
- **[`get_user_top_artists`](api/client.md#client.LastFM.get_user_top_artists)**: the top artists of a user over a specific range of time (`'overall', '7day', '1month', '3month', '6month', '12month'`).
- **[`get_user_top_tags`](api/client.md#client.LastFM.get_user_top_tags)**: the top tags of a user.
- **[`get_user_top_tracks`](api/client.md#client.LastFM.get_user_top_tracks)**: the top tracks of a user over a specific range of time (`'overall', '7day', '1month', '3month', '6month', '12month'`).
- **[`get_user_weekly_album_chart`](api/client.md#client.LastFM.get_user_weekly_album_chart)**: the user's weekly albums chart with optional date filtering.
- **[`get_user_weekly_artist_chart`](api/client.md#client.LastFM.get_user_weekly_artist_chart)**: the user's weekly artists chart with optional date filtering.
- **[`get_user_weekly_track_chart`](api/client.md#client.LastFM.get_user_weekly_track_chart)**: the user's weekly tracks chart with optional date filtering.

## What is not implemented

There are some methods available in LastFM API backend that are not implemented in this package.

- `album.addTags`
- `album.removeTag`
- `artist.addTags`
- `artist.removeTag`
- `auth.getMobileSession`
- `auth.getSession`
- `auth.getToken`
- `tag.getTopTags`
- `tag.getWeeklyChartList`
- `track.addTags`
- `track.love`
- `track.removeTag`
- `track.scrobble`
- `track.unlove`
- `track.updateNowPlaying`
- `user.getWeeklyChartList`

The `tag.getWeeklyChartList` and `user.getWeeklyChartList` methods were ignored, because this package does not handle weeks, but with specific dates.
So the fetched data from these methods are useless to the user. 

The others are POST and authentication methods. Feel free to add them, learn how to contribute [here](contribution.md).
