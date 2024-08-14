from datetime import datetime

import pytest

from pylastfmapi.exceptions import LastFMException
from pylastfmapi.utils import get_timestamp

#########################################################################
# get_timestamp
#########################################################################


def test_get_timestamp_with_wrong_date_from_date_to():
    date_from = '2023-40-10'
    date_to = '2023-40-11'
    ##
    with pytest.raises(
        LastFMException,
        match='The params "date_from" and "date_to" should be a valid date'
        ' and in "YYYY-MM-DD" or "YYYY-MM-DD %H:%M" format: time data '
        "'2023-40-10' does not match format '%Y-%m-%d'",
    ):
        _ = get_timestamp(date_from=date_from, date_to=date_to)


def test_get_timestamp_with_date_from_higher_than_date_to():
    date_from = '2023-05-10'
    date_to = '2023-04-10'
    ##
    with pytest.raises(
        LastFMException,
        match='The params "date_from" should be lower than "date_to"',
    ):
        _ = get_timestamp(date_from=date_from, date_to=date_to)


@pytest.mark.parametrize(
    ('date_from', 'date_to'),
    [
        ('2023-04-10', None),
        (None, '2023-04-10'),
    ],
)
def test_get_timestamp_without_one_date(date_from, date_to):
    ##
    with pytest.raises(
        LastFMException,
        match='The params "date_from" and "date_to" should be given together',
    ):
        _ = get_timestamp(date_from=date_from, date_to=date_to)


@pytest.mark.parametrize(
    ('date_from', 'format_from', 'date_to', 'format_to'),
    [
        ('2023-03-10 10:10', '%Y-%m-%d %H:%M', '2024-08-07', '%Y-%m-%d'),
        ('2023-03-10', '%Y-%m-%d', '2024-08-07 10:10', '%Y-%m-%d %H:%M'),
    ],
)
def test_get_timestamp_date_with_format_with_hour(
    date_from, format_from, date_to, format_to
):
    ##
    response = get_timestamp(date_from=date_from, date_to=date_to)
    ##
    assert response[0] == int(
        datetime.strptime(date_from, format_from).timestamp()
    )
    assert response[1] == int(
        datetime.strptime(date_to, format_to).timestamp()
    )
