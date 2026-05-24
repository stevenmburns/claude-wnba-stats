"""Tests for the DuckDB wrapper. The sportsdataverse-py loaders are
mocked so nothing hits the network."""

from unittest.mock import patch

import pandas as pd
import pytest

from claude_wnba_stats import db


@pytest.fixture
def fake_loaders():
    """Patch data.* at db's import binding so db._load uses fake data."""
    sched = pd.DataFrame({"game_id": [1, 2], "home_display_name": ["A", "B"]})
    team = pd.DataFrame({"game_id": [1, 2], "team_name": ["X", "Y"], "points": [80, 90]})
    player = pd.DataFrame(
        {
            "game_id": [1, 1, 2],
            "athlete_display_name": ["P1", "P2", "P1"],
            "points": [20, 15, 25],
            "did_not_play": [False, False, False],
        }
    )
    with (
        patch("claude_wnba_stats.db.data.schedule", return_value=sched) as ms,
        patch("claude_wnba_stats.db.data.team_boxscores", return_value=team) as mt,
        patch("claude_wnba_stats.db.data.player_boxscores", return_value=player) as mp,
    ):
        yield ms, mt, mp


def test_connect_registers_three_tables(fake_loaders) -> None:
    con = db.connect([2024])
    tables = {row[0] for row in con.sql("SHOW TABLES").fetchall()}
    assert {"schedule", "team_boxscores", "player_boxscores"} <= tables


def test_connect_tables_are_queryable(fake_loaders) -> None:
    con = db.connect([2024])
    assert con.sql("SELECT COUNT(*) FROM schedule").fetchone()[0] == 2
    assert con.sql("SELECT COUNT(*) FROM team_boxscores").fetchone()[0] == 2
    assert con.sql("SELECT COUNT(*) FROM player_boxscores").fetchone()[0] == 3


def test_query_returns_dataframe(fake_loaders) -> None:
    df = db.query("SELECT SUM(points) AS total FROM player_boxscores", [2024])
    assert isinstance(df, pd.DataFrame)
    assert df["total"].iloc[0] == 60


def test_query_supports_joins_across_tables(fake_loaders) -> None:
    df = db.query(
        """
        SELECT s.home_display_name, COUNT(p.athlete_display_name) AS rows
        FROM schedule s
        JOIN player_boxscores p USING (game_id)
        GROUP BY s.home_display_name
        ORDER BY s.home_display_name
        """,
        [2024],
    )
    assert list(df["home_display_name"]) == ["A", "B"]
    assert list(df["rows"]) == [2, 1]


def test_load_caches_per_seasons_tuple(fake_loaders) -> None:
    ms, mt, mp = fake_loaders
    db.query("SELECT 1", [2024])
    db.query("SELECT 1", [2024])
    assert ms.call_count == 1
    assert mt.call_count == 1
    assert mp.call_count == 1


def test_seasons_order_does_not_affect_cache_key(fake_loaders) -> None:
    ms, _, _ = fake_loaders
    db.query("SELECT 1", [2023, 2024])
    db.query("SELECT 1", [2024, 2023])
    assert ms.call_count == 1


def test_different_seasons_trigger_separate_loads(fake_loaders) -> None:
    ms, _, _ = fake_loaders
    db.query("SELECT 1", [2023])
    db.query("SELECT 1", [2024])
    assert ms.call_count == 2
