class LastFMException(Exception):
    """
    Base exception for all LastFM API client-related errors.

    It can be used to catch general LastFM-related errors in your
    application.
    """


class RequestErrorException(Exception):
    """
    Exception raised for errors related to HTTP requests to the LastFM API
    backend.

    This exception is triggered when an HTTP request to the LastFM API fails,
    such as due to network issues, timeouts, or invalid responses from the API.
    """
