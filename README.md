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

## Test

```bash
pytest
```
