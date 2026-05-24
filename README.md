# claude-wnba-stats

WNBA stats exploration built on [sportsdataverse-py](https://py.sportsdataverse.org/).

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Use

```bash
wnba-stats schedule 2024
wnba-stats team-boxscores 2023 2024
wnba-stats player-boxscores 2024 --head 5
```

Or from Python:

```python
from claude_wnba_stats import data

df = data.player_boxscores([2024])
print(df.head())
```

## SQL via DuckDB

The same data is also queryable as SQL. Tables: `schedule`, `team_boxscores`, `player_boxscores`.

```python
from claude_wnba_stats import db

db.query("""
    SELECT athlete_display_name, SUM(points) AS pts
    FROM player_boxscores
    WHERE NOT did_not_play
    GROUP BY athlete_display_name
    ORDER BY pts DESC
    LIMIT 10
""", seasons=[2026])
```

Or from the CLI:

```bash
wnba-stats sql "SELECT athlete_display_name, points FROM player_boxscores ORDER BY points DESC LIMIT 5" --seasons 2026
```

For multi-query sessions, grab a connection directly:

```python
con = db.connect([2026])
con.sql("SELECT COUNT(*) FROM player_boxscores").show()
```

## Test

```bash
pytest
```
