"""Format raw result rows into structured dicts."""

import re
from datetime import datetime

from full_time_api.date_types import DATE, FULL_TIME_DATE, TIME


class ResultFormatter:
    """Format result rows with optional date/time formats."""

    def format_results(
        self,
        results: list[list[str]],
        date_format: str | None = None,
        time_format: str | None = None,
    ) -> list[dict]:
        """
        results: list of [datetime, home, score, away, division].
        """
        date_fmt = date_format or DATE
        time_fmt = time_format or TIME
        formatted: list[dict] = []

        for result in results:
            if len(result) < 4:
                continue
            try:
                dt = datetime.strptime(result[0], FULL_TIME_DATE)
                fixture_date = dt.strftime(date_fmt)
                fixture_time = dt.strftime(time_fmt)
            except ValueError:
                continue
            score_str = result[2]
            home_score = ""
            away_score = ""
            if score_str:
                home_match = re.search(r"(\d+)", score_str)
                away_match = re.search(r"(\d+)(?!.*\d)", score_str)
                if home_match:
                    home_score = home_match.group(1)
                if away_match:
                    away_score = away_match.group(1)
            formatted.append({
                "Date": fixture_date,
                "Time": fixture_time,
                "Home": result[1],
                "HomeScore": home_score,
                "Away": result[3],
                "AwayScore": away_score,
                "FullScore": score_str,
            })
        return formatted
