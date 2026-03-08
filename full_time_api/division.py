"""Division API: teams, fixtures, and results with optional formatting."""

from full_time_api.client import FullTimeClient
from full_time_api.formatters import FixtureFormatter, ResultFormatter
from full_time_api.fixtures import Fixtures
from full_time_api.results import Results
from full_time_api.teams import Teams


class Division:
    """Entry point for FA Full-Time division data: teams, fixtures, results."""

    def __init__(self, client: FullTimeClient | None = None) -> None:
        self._client = client or FullTimeClient()
        self._formatter = ResultFormatter()
        self._teams = Teams(self._client)
        self._fixtures = Fixtures(self._client)
        self._results = Results(self._client)

    def get_teams(self, season_id: int, group_id: str) -> list[str]:
        """Return list of team names for the given season and group."""
        return self._teams.get_teams(season_id, group_id)

    def get_fixtures(self, season_id: int, group_id: str) -> list[list[str]]:
        """Return raw fixture rows (list of cell lists)."""
        return self._fixtures.get_fixtures(season_id, group_id)

    def get_results(self, season_id: int, group_id: str) -> list[list[str]]:
        """Return raw result rows [datetime, home, score, away, division]."""
        return self._results.get_results(season_id, group_id)

    def get_formatted_fixtures(
        self,
        season_id: int,
        group_id: str,
        formatter: FixtureFormatter | None = None,
        include_tbc_fixtures: bool = True,
        include_cup_fixtures: bool = True,
        date_format: str | None = None,
        time_format: str | None = None,
    ) -> list[dict]:
        """Return fixtures as list of dicts (Date, Home, Away, Time, FixtureType)."""
        fmt = formatter or FixtureFormatter()
        raw = self._fixtures.get_fixtures(season_id, group_id)
        return fmt.format_fixtures(
            raw,
            include_tbc_fixtures=include_tbc_fixtures,
            include_cup_fixtures=include_cup_fixtures,
            date_format=date_format,
            time_format=time_format,
        )

    def get_formatted_results(
        self,
        season_id: int,
        group_id: str,
        date_format: str | None = None,
        time_format: str | None = None,
    ) -> list[dict]:
        """Return results as list of dicts (Date, Time, Home, HomeScore, Away, AwayScore, FullScore)."""
        raw = self._results.get_results(season_id, group_id)
        return self._formatter.format_results(
            raw,
            date_format=date_format,
            time_format=time_format,
        )
