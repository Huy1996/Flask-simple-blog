import pytest
from datetime import datetime
from utils import date_filter


def test_valid_date():
    day = datetime(year=1996, month=11, day=10)
    date_fmt = date_filter(day)
    assert date_fmt == "November 10, 1996"


def test_invalid_arg():
    with pytest.raises(ValueError):
        date_fmt = date_filter("Some string")


@pytest.mark.parametrize('date', [
    datetime(2000, 10, 20), datetime.utcnow(), datetime.now()])
def test_filter(date):
    try:
        assert type(date_filter(date)) == str
    except ValueError:
        assert False