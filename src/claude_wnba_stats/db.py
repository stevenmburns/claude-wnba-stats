"""DuckDB-backed SQL access to sportsdataverse-py WNBA data.

Builds an in-memory DuckDB connection with three tables registered:
`schedule`, `team_boxscores`, `player_boxscores`. The underlying pandas
DataFrames are loaded once per seasons tuple and cached.
"""

from __future__ import annotations

from functools import lru_cache

import duckdb
import pandas as pd

from . import data


@lru_cache(maxsize=8)
def _load(seasons: tuple[int, ...]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    seasons_list = list(seasons)
    return (
        data.schedule(seasons_list),
        data.team_boxscores(seasons_list),
        data.player_boxscores(seasons_list),
    )


def connect(seasons: list[int]) -> duckdb.DuckDBPyConnection:
    """Return an in-memory DuckDB connection with WNBA tables registered.

    Tables: `schedule`, `team_boxscores`, `player_boxscores`.
    """
    sched, team, player = _load(tuple(sorted(seasons)))
    con = duckdb.connect(":memory:")
    con.register("schedule", sched)
    con.register("team_boxscores", team)
    con.register("player_boxscores", player)
    return con


def query(sql: str, seasons: list[int]) -> pd.DataFrame:
    """Run a one-shot SQL query and return the result as a DataFrame."""
    return connect(seasons).sql(sql).df()
