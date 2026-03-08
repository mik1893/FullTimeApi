"""Teams from Full-Time."""

from full_time_api.client import FullTimeClient
from full_time_api.helpers import remove_whitespace
from full_time_api.xpath_helpers import create_dom_xpath


class Teams:
    """Fetch and parse team list for a season/group."""

    def __init__(self, client: FullTimeClient) -> None:
        self._client = client

    def get_teams(self, season_id: int, group_id: str) -> list[str]:
        """Return list of team names."""
        url = (
            "https://fulltime.thefa.com/fixtures.html?"
            f"selectedSeason={season_id}&selectedFixtureGroupKey={group_id}"
            "&selectedDateCode=all&selectedRelatedFixtureOption=1&itemsPerPage=100"
        )
        data = self._client.get(url)
        return self.extract_teams(data)

    def extract_teams(self, data: str) -> list[str]:
        """Parse fixtures HTML and return option text from team dropdown."""
        doc = create_dom_xpath(data)
        team_nodes = doc.xpath('//*[@id="form1_selectedTeam"]/option')
        return [remove_whitespace(n.text_content() or "") for n in team_nodes]
