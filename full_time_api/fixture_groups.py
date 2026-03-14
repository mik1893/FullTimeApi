"""Fixture groups from a league page."""

from full_time_api.client import FullTimeClient
from full_time_api.helpers import remove_whitespace
from full_time_api.xpath_helpers import create_dom_xpath


class FixtureGroups:
    """Fetch and parse fixture groups for a league/season."""

    def __init__(self, client: FullTimeClient) -> None:
        self._client = client

    def get_fixture_groups(
        self, league_id: int, season_id: int
    ) -> list[dict[str, str]]:
        """
        Return list of fixture groups with id and name.

        Fetches the league fixtures page and parses the fixture group dropdown.
        Excludes the 'All' option. Each item is {"id": "...", "name": "..."}.
        """
        url = (
            "https://fulltime.thefa.com/fixtures.html?"
            f"league={league_id}&selectedSeason={season_id}"
        )
        data = self._client.get(url)
        return self._extract_fixture_groups(data)

    def _extract_fixture_groups(self, data: str) -> list[dict[str, str]]:
        doc = create_dom_xpath(data)
        options = doc.xpath(
            '//*[@id="form1_selectedFixtureGroupKey"]/option'
        )
        groups: list[dict[str, str]] = []
        for opt in options:
            value = (opt.get("value") or "").strip()
            if not value:
                continue
            name = remove_whitespace(opt.text_content() or "")
            groups.append({"id": value, "name": name})
        return groups
