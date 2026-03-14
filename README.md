# full-time-api (Python)

A simple tool to obtain fixture information from the FA Full-Time system.

## Requirements

- Python >= 3.8

## Installation

```bash
pip install full-time-api
```

Or from source in this directory:

```bash
pip install .
```

## Getting season and group IDs

You need a **Season ID** and **Group ID** from Full-Time. Open the division page on [fulltime.thefa.com](https://fulltime.thefa.com) and take them from the URL:

- `selectedSeason=1234` → season ID `1234`
- `FixtureGroupKey=1_234` → group ID `1_234`

## Usage

```python
from full_time_api import Division

division = Division()

# Team list
teams = division.get_teams(1234, "1_234")

# Raw fixtures (list of rows, each row is list of cell strings)
fixtures = division.get_fixtures(1234, "1_234")

# Formatted fixtures (list of dicts: Date, Home, Away, Time, FixtureType)
fixtures = division.get_formatted_fixtures(1234, "1_234")

# Raw results
results = division.get_results(1234, "1_234")

# Formatted results (list of dicts: Date, Time, Home, HomeScore, Away, AwayScore, FullScore)
results = division.get_formatted_results(1234, "1_234")
```

### Optional formatting

```python
# Custom date/time format (strftime-style)
results = division.get_formatted_results(
    1234, "1_234",
    date_format="%Y-%m-%d",
    time_format="%H:%M"
)

# Formatted fixtures: exclude TBC or cup fixtures, custom formatter
from full_time_api.formatters import FixtureFormatter

fixtures = division.get_formatted_fixtures(
    1234, "1_234",
    formatter=FixtureFormatter(),
    include_tbc_fixtures=True,
    include_cup_fixtures=False,
    date_format="%d/%m/%Y",
    time_format="%H:%M"
)
```

### Using your own HTTP client

```python
from full_time_api import FullTimeClient, Division

# Division uses FullTimeClient() by default; you can pass a custom one
# if you need different timeouts or session config (extend FullTimeClient).
division = Division(client=FullTimeClient())
```

## License

MIT (same as the original PHP package).
