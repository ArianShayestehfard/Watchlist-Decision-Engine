from omdb_api import parse_release_date, parse_runtime


def test_parse_release_date_valid():
    assert parse_release_date("07 Nov 2014") == "2014-11-07"


def test_parse_release_date_invalid_format():
    assert parse_release_date("N/A") is None


def test_parse_release_date_none():
    assert parse_release_date(None) is None


def test_parse_runtime_valid():
    assert parse_runtime("169 min") == 169


def test_parse_runtime_invalid():
    assert parse_runtime("N/A") is None


def test_parse_runtime_none():
    assert parse_runtime(None) is None
