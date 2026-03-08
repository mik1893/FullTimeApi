"""Format raw fixture rows into structured dicts."""

from datetime import datetime

from full_time_api.date_types import DATE, FULL_TIME_DATE, TIME


class FixtureFormatter:
    """Format fixture rows with optional date/time formats and filters."""

    def format_fixtures(
        self,
        fixtures: list[list[str]],
        include_tbc_fixtures: bool = True,
        include_cup_fixtures: bool = True,
        date_format: str | None = None,
        time_format: str | None = None,
    ) -> list[dict]:
        """
        fixtures: list of rows (each row: [FixtureType, DateTime, Home, ..., Away, ...]).
        Indices: 0=type, 1=date/time, 2=home, 6=away.
        """
        date_fmt = date_format or DATE
        time_fmt = time_format or TIME
        formatted: list[dict] = []

        for fixture in fixtures:
            if not fixture:
                continue
            if not include_cup_fixtures and fixture[0] == "Cup":
                continue
            if include_tbc_fixtures and fixture[1] == "TBC":
                formatted.append({
                    "Date": "TBC",
                    "Home": fixture[2] if len(fixture) > 2 else "",
                    "Away": fixture[6] if len(fixture) > 6 else "",
                    "Time": "TBC",
                    "FixtureType": fixture[0],
                })
                continue
            try:
                dt = datetime.strptime(fixture[1], FULL_TIME_DATE)
                fixture_date = dt.strftime(date_fmt)
                fixture_time = dt.strftime(time_fmt)
            except (ValueError, IndexError):
                continue
            formatted.append({
                "Date": fixture_date,
                "Home": fixture[2] if len(fixture) > 2 else "",
                "Away": fixture[6] if len(fixture) > 6 else "",
                "Time": fixture_time,
                "FixtureType": fixture[0],
            })
        return formatted
