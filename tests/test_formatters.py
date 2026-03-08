"""Tests for formatters (mirror of PHP FixtureFormatterTest and ResultFormatterTest)."""

import pytest
from full_time_api.formatters import FixtureFormatter, ResultFormatter


def test_fixture_formatter():
    formatter = FixtureFormatter()
    raw = [
        ["L", "05/02/22 09:10", "Rosegrove FC - Rangers U7S", "", "VS", "", "Rossendale United - Yellow U7S", "", "UNDER 07S", ""],
        ["L", "12/03/22 09:55", "Rossendale United - Yellow U7S", "", "VS", "", "Junior Hoops JFC - Cobras U7S", "", "UNDER 07S", ""],
        ["Cup", "12/01/22 13:00", "Woods FC - Yellow U7S", "", "VS", "", "Junior Hoops JFC - Cobras U7S", "", "UNDER 07S", ""],
    ]
    expected = [
        {"Date": "05/02/2022", "Home": "Rosegrove FC - Rangers U7S", "Away": "Rossendale United - Yellow U7S", "Time": "09:10", "FixtureType": "L"},
        {"Date": "12/03/2022", "Home": "Rossendale United - Yellow U7S", "Away": "Junior Hoops JFC - Cobras U7S", "Time": "09:55", "FixtureType": "L"},
        {"Date": "12/01/2022", "Home": "Woods FC - Yellow U7S", "Away": "Junior Hoops JFC - Cobras U7S", "Time": "13:00", "FixtureType": "Cup"},
    ]
    assert formatter.format_fixtures(raw) == expected


def test_result_formatter():
    formatter = ResultFormatter()
    raw = [
        ["29/05/21 09:30", "Mill Hill Juniors - Red U14S", "0 - 2", "Wilpshire Wanderers - Blue U14S", "SURRIDGE SPORTS U14S CUP 2020 - 2021"],
        ["22/05/21 11:30", "Wilpshire Wanderers - Red U14S", "2 - 2", "Rosegrove FC - Warriors U14S", "UNDER 14S"],
    ]
    expected = [
        {"Date": "29/05/2021", "Time": "09:30", "Home": "Mill Hill Juniors - Red U14S", "HomeScore": "0", "Away": "Wilpshire Wanderers - Blue U14S", "AwayScore": "2", "FullScore": "0 - 2"},
        {"Date": "22/05/2021", "Time": "11:30", "Home": "Wilpshire Wanderers - Red U14S", "HomeScore": "2", "Away": "Rosegrove FC - Warriors U14S", "AwayScore": "2", "FullScore": "2 - 2"},
    ]
    assert formatter.format_results(raw) == expected
