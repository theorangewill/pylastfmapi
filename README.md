# pylastfm 

This package provides an interface to interact with the LastFM API.
It includes methods to retrieve various types of data from albums, artists, tracks, tags, users, LastFM charts, and user charts. 
The package supports pagination for large datasets and provides flexibility in querying data with optional filters, following the parameters provided by the API.

## Installation

To install the package, use the following command:

```{.sh}
pip install pylastfm
```
## Basic usage

### Get an API key
First of all, you need to get an API key from LastFM official website. For this, you will need a LastFM account [here](https://www.last.fm/join). With your user profile, create an API account [here](https://www.last.fm/api/account/create); you only need the contact email and application name and an API key will be given to you.

### Go to Python script

To interact with the LastFM API you can simply import `pylastfm` and create a LastFM client object with your username as `USER_AGENT` and the API key from the previous step as `API_KEY`:

```{.py3}
from pylastfm.client import LastFM

# Your LastFM API credentials
USER_AGENT = 'user-agent'
API_KEY = 'api-key'

# Initialize the LastFM client with your USER_AGENT and API_KEY
client = LastFM(USER_AGENT, API_KEY)

# Fetch information about a specific artist
artist_info = client.get_artist_info(artist="Miley Cyrus")
print(artist_info)
# {'name': 'Miley Cyrus', 'mbid': '7e9bd05a-117f-4cce-8...
```

## Error Handling

The package raises `LastFMException` for various error conditions such as invalid parameters or request limits.
Handle these exceptions to ensure your application can gracefully manage errors.
