"""Fixtures from Full-Time."""

from full_time_api.client import FullTimeClient
from full_time_api.helpers import remove_whitespace
from full_time_api.xpath_helpers import create_dom_xpath


class Fixtures:
    """Fetch and parse fixtures for a season/group."""

    def __init__(self, client: FullTimeClient) -> None:
        self._client = client

    def get_fixtures(self, season_id: int, group_id: str) -> list[list[str]]:
        """Return list of fixture rows (each row is a list of cell strings)."""
        url = (
            "https://fulltime.thefa.com/fixtures.html?"
            f"selectedSeason={season_id}&selectedFixtureGroupKey={group_id}"
            "&selectedDateCode=all&selectedRelatedFixtureOption=1"
            f"&previousSelectedFixtureGroupKey={group_id}&itemsPerPage=10000"
        )
        data = self._client.get(url)
        return self._extract_fixtures(data)

    def _extract_fixtures(self, data: str) -> list[list[str]]:
        doc = create_dom_xpath(data)
        rows = doc.xpath("//table//tr")
        fixtures: list[list[str]] = []
        for row in rows:
            cells = row.findall("td")
            if not cells:
                continue
            fixture = [remove_whitespace(c.text or "") for c in cells]
            if any(fixture):
                fixtures.append(fixture)
        return fixtures
