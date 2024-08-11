# pylastfm

This package provides an interface for interacting with the LastFM API.
It includes methods to retrieve various types of data from albums, artists, tracks, tags, users and LastFM charts, user track charts. 
The package supports pagination for large datasets and provides flexibility in querying data with optional filters, following the parameters provided by the API.

## Installation

To install the package, use the following command:

```{.sh}
pip install pylastfm
```

## Usage

## Error Handling

The package raises `LastFMException` for various error conditions such as invalid parameters or request limits.
Handle these exceptions to ensure your application can gracefully manage errors.
