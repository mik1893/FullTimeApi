"""Results from Full-Time."""

from full_time_api.client import FullTimeClient
from full_time_api.helpers import remove_whitespace
from full_time_api.xpath_helpers import create_dom_xpath


class Results:
    """Fetch and parse results for a season/group."""

    def __init__(self, client: FullTimeClient) -> None:
        self._client = client

    def get_results(self, season_id: int, group_id: str) -> list[list[str]]:
        """Return list of result rows [datetime, home, score, away, division]."""
        url = (
            "https://fulltime.thefa.com/results.html?"
            f"selectedSeason={season_id}&selectedFixtureGroupKey={group_id}"
            "&selectedDateCode=all&selectedRelatedFixtureOption=1"
            f"&previousSelectedFixtureGroupKey={group_id}&itemsPerPage=10000"
        )
        data = self._client.get(url)
        return self.extract_results(data)

    def extract_results(self, data: str) -> list[list[str]]:
        """Parse results HTML into list of [datetime, home, score, away, division]."""
        doc = create_dom_xpath(data)
        # Same structure as PHP: //*[@id="results-list"]/div/div[3]/div/div[2]/div
        result_nodes = doc.xpath('//*[@id="results-list"]/div/div[3]/div/div[2]/div')
        return [self._extract_fixture_result(node) for node in result_nodes]

    def _extract_fixture_result(self, node) -> list[str]:
        def text(q: str) -> str:
            found = node.xpath(q)
            return (found[0].text_content() or "").strip() if found else ""

        fixture_date_time = remove_whitespace(
            text('.//div[contains(@class, "datetime-col")]')
        )
        home_team = text('.//div[contains(@class, "home-team-col")]')
        away_team = text('.//div[contains(@class, "road-team-col")]')
        score = text('.//div[contains(@class, "score-col")]')
        division = text('.//div[contains(@class, "fg-col")]')
        return [fixture_date_time, home_team, score, away_team, division]
