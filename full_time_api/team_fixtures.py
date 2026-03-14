"""Team fixtures from Full-Time (all fixtures for a single team)."""

from datetime import datetime
from urllib.parse import parse_qs, urlparse

from full_time_api.client import FullTimeClient
from full_time_api.helpers import remove_whitespace
from full_time_api.xpath_helpers import create_dom_xpath

# Same format as elsewhere: dd/mm/yy HH:MM
_FULL_TIME_DATETIME = "%d/%m/%y %H:%M"
_DATE_OUT = "%d/%m/%Y"
_TIME_OUT = "%H:%M"

HEADER_ROW = [
    "Season ID",
    "Team ID",
    "Fixture ID",
    "Type",
    "Date",
    "Time",
    "Home Team",
    "Away Team",
    "Venue",
    "Competition",
    "Status",
    "Is Home Match",
]


class TeamFixtures:
    """Fetch and parse all fixtures for a team in a season."""

    def __init__(self, client: FullTimeClient) -> None:
        self._client = client

    def get_team_fixtures(
        self, season_id: int, team_id: int
    ) -> list[list[str]]:
        """
        Return team fixtures as a list of rows with header.

        First row is HEADER_ROW. Each data row has: Season ID, Team ID, Fixture ID, Type, Date, Time,
        Home Team, Away Team, Venue, Competition, Status, Is Home Match.
        Date/Time is split from the page column; VS column omitted;
        Is Home Match is "Yes" when the selected team is the home team.
        """
        url = (
            "https://fulltime.thefa.com/fixtures.html?"
            "selectedSeason={}&selectedFixtureGroupAgeGroup=0"
            "&selectedFixtureGroupKey=&selectedDateCode=all&selectedClub="
            "&selectedTeam={}&selectedRelatedFixtureOption=3"
            "&selectedFixtureDateStatus=&selectedFixtureStatus="
            "&previousSelectedFixtureGroupAgeGroup=&previousSelectedFixtureGroupKey="
            "&itemsPerPage=10000"
        ).format(season_id, team_id)
        data = self._client.get(url)
        return self._extract_team_fixtures(data, season_id, team_id)

    def _extract_team_fixtures(
        self, data: str, season_id: int, team_id: int
    ) -> list[list[str]]:
        doc = create_dom_xpath(data)
        team_name = self._get_selected_team_name(doc)
        divs = doc.xpath("//div[contains(@class, 'fixtures-table')]")
        if not divs:
            return [HEADER_ROW]
        tables = divs[0].xpath(".//table")
        if not tables:
            return [HEADER_ROW]
        rows = tables[0].xpath(".//tr")
        result: list[list[str]] = [HEADER_ROW]
        for row in rows:
            cells = row.findall("td")
            if not cells:
                continue
            raw = [remove_whitespace(c.text_content() or "") for c in cells]
            if len(raw) < 9:
                continue
            # Columns: 0=Type, 1=Date/Time, 2=Home, 3=empty, 4=score (VS link), 5=empty, 6=Away, 7=Venue, 8=Competition, 9=Status
            fixture_id = _extract_fixture_id(cells[4])
            date_str, time_str = _split_date_time(raw[1])
            home_team = raw[2]
            away_team = raw[6]
            is_home = "Yes" if home_team == team_name else "No"
            result.append([
                str(season_id),
                str(team_id),
                fixture_id,
                raw[0],       # Type
                date_str,
                time_str,
                home_team,
                away_team,
                raw[7],       # Venue
                raw[8],       # Competition
                raw[9],       # Status
                is_home,
            ])
        return result

    def _get_selected_team_name(self, doc) -> str:
        options = doc.xpath(
            '//*[@id="form1_selectedTeam"]/option[@selected]'
        )
        if options:
            return remove_whitespace(options[0].text_content() or "")
        return ""


def _extract_fixture_id(score_cell) -> str:
    """Extract fixture id from displayFixture.html?id=... link in the score td."""
    links = score_cell.xpath(".//a[starts-with(@href, '/displayFixture.html')]")
    if not links:
        return ""
    href = links[0].get("href") or ""
    parsed = urlparse(href)
    qs = parse_qs(parsed.query)
    ids = qs.get("id", [])
    return ids[0] if ids else ""


def _split_date_time(date_time: str) -> tuple[str, str]:
    """Split 'dd/mm/yy HH:MM' into (date dd/mm/yyyy, time HH:MM)."""
    date_time = date_time.strip()
    if not date_time or date_time.upper() == "TBC":
        return ("", "")
    try:
        dt = datetime.strptime(date_time, _FULL_TIME_DATETIME)
        return (dt.strftime(_DATE_OUT), dt.strftime(_TIME_OUT))
    except ValueError:
        return (date_time, "")
