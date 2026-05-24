"""Thin wrappers around sportsdataverse-py WNBA loaders."""

from __future__ import annotations

import pandas as pd
from sportsdataverse.wnba import (
    load_wnba_player_boxscore,
    load_wnba_schedule,
    load_wnba_team_boxscore,
)


def schedule(seasons: list[int]) -> pd.DataFrame:
    """Game schedule + results for the given seasons."""
    return load_wnba_schedule(seasons=seasons, return_as_pandas=True)


def team_boxscores(seasons: list[int]) -> pd.DataFrame:
    """Per-team, per-game box scores for the given seasons."""
    return load_wnba_team_boxscore(seasons=seasons, return_as_pandas=True)


def player_boxscores(seasons: list[int]) -> pd.DataFrame:
    """Per-player, per-game box scores for the given seasons."""
    return load_wnba_player_boxscore(seasons=seasons, return_as_pandas=True)
