from datetime import datetime

from pylastfm.exceptions import LastFMException


def get_timestamp(
    date_from: str | None, date_to: str | None
) -> tuple[int | None, int | None]:
    """
    Convert date strings to UNIX timestamps.

    This function takes two date strings, `date_from` and `date_to`, and
    converts them to UNIX timestamps.
    The dates must be provided together and should be in one of the
    following formats:

    - "YYYY-MM-DD"
    - "YYYY-MM-DD HH:MM"

    If either date is not provided, or if `date_from` is greater than
    or equal to `date_to`, the function will raise a `LastFMException`.

    Args:
        date_from (str): The starting date string to convert.
            Must be in "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            If `None`, both `date_from` and `date_to` must be `None`.
        date_to (str): The ending date string to convert.
            Must be in "YYYY-MM-DD" or "YYYY-MM-DD HH:MM" format.
            If `None`, both `date_from` and `date_to` must be `None`.

    Returns:
        A tuple containing the UNIX timestamps for `date_from` and `date_to`.

    Raises:
        LastFMException:
            - If the date format is invalid.
            - If `date_from` is greater than or equal to `date_to`.
            - If only one of `date_from` or `date_to` is provided.

    """
    if date_from and date_to:

        def _convert_date(date: str) -> int:
            try:
                if len(date) == len('YYYY-MM-DD'):
                    timestamp = datetime.strptime(date, '%Y-%m-%d')
                else:
                    timestamp = datetime.strptime(date, '%Y-%m-%d %H:%M')
            except ValueError as e:
                raise LastFMException(
                    'The params "date_from" and "date_to" should be a '
                    'valid date and in "YYYY-MM-DD" or "YYYY-MM-DD %H:%M" '
                    f'format: {e}'
                )
            else:
                return int(timestamp.timestamp())

        timestamp_from = _convert_date(date_from)
        timestamp_to = _convert_date(date_to)
        if timestamp_from >= timestamp_to:
            raise LastFMException(
                'The params "date_from" should be lower than "date_to"'
            )
    elif date_from or date_to:
        raise LastFMException(
            'The params "date_from" and "date_to" should be given ' 'together'
        )
    else:
        timestamp_from, timestamp_to = None, None
    return timestamp_from, timestamp_to
