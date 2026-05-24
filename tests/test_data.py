"""Tests for the sportsdataverse-py wrappers in `data.py`. The functions
are intentionally thin, so the tests pin down the call contract (correct
args forwarded, return value passed through)."""

from unittest.mock import patch

import pandas as pd

from claude_wnba_stats import data


def test_schedule_forwards_args_and_returns_dataframe() -> None:
    fake = pd.DataFrame({"game_id": [1, 2]})
    with patch("claude_wnba_stats.data.load_wnba_schedule", return_value=fake) as m:
        result = data.schedule([2023, 2024])
    m.assert_called_once_with(seasons=[2023, 2024], return_as_pandas=True)
    assert result is fake


def test_team_boxscores_forwards_args_and_returns_dataframe() -> None:
    fake = pd.DataFrame({"game_id": [1], "team_name": ["X"]})
    with patch("claude_wnba_stats.data.load_wnba_team_boxscore", return_value=fake) as m:
        result = data.team_boxscores([2024])
    m.assert_called_once_with(seasons=[2024], return_as_pandas=True)
    assert result is fake


def test_player_boxscores_forwards_args_and_returns_dataframe() -> None:
    fake = pd.DataFrame({"game_id": [1], "athlete_display_name": ["P1"]})
    with patch("claude_wnba_stats.data.load_wnba_player_boxscore", return_value=fake) as m:
        result = data.player_boxscores([2024])
    m.assert_called_once_with(seasons=[2024], return_as_pandas=True)
    assert result is fake
