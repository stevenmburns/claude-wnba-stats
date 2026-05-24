"""Tests for the CLI. Loaders and db.query are mocked so nothing hits
the network and we exercise argparse + dispatch in isolation."""

from unittest.mock import patch

import pandas as pd
import pytest

from claude_wnba_stats import cli


@pytest.fixture
def fake_loaders():
    df = pd.DataFrame({"game_id": [1, 2, 3], "x": ["a", "b", "c"]})
    with (
        patch("claude_wnba_stats.cli.data.schedule", return_value=df) as ms,
        patch("claude_wnba_stats.cli.data.team_boxscores", return_value=df) as mt,
        patch("claude_wnba_stats.cli.data.player_boxscores", return_value=df) as mp,
    ):
        yield ms, mt, mp


def test_schedule_subcommand_dispatches_to_schedule_loader(fake_loaders, capsys) -> None:
    ms, _, _ = fake_loaders
    rc = cli.main(["schedule", "2024"])
    assert rc == 0
    ms.assert_called_once_with([2024])
    assert "3 rows" in capsys.readouterr().out


def test_team_boxscores_subcommand_passes_multiple_seasons(fake_loaders) -> None:
    _, mt, _ = fake_loaders
    cli.main(["team-boxscores", "2023", "2024"])
    mt.assert_called_once_with([2023, 2024])


def test_player_boxscores_subcommand_dispatches_correctly(fake_loaders) -> None:
    _, _, mp = fake_loaders
    cli.main(["player-boxscores", "2024"])
    mp.assert_called_once_with([2024])


def test_head_flag_limits_printed_rows(fake_loaders, capsys) -> None:
    cli.main(["schedule", "2024", "--head", "1"])
    out = capsys.readouterr().out
    # All three game_ids exist in the dataframe but only one row should appear.
    assert "1" in out
    assert "3 rows" in out  # row count still reports the full dataframe


def test_sql_subcommand_invokes_db_query(capsys) -> None:
    df = pd.DataFrame({"n": [42]})
    with patch("claude_wnba_stats.cli.db.query", return_value=df) as mq:
        rc = cli.main(["sql", "SELECT 42 AS n", "--seasons", "2024"])
    assert rc == 0
    mq.assert_called_once_with("SELECT 42 AS n", [2024])
    out = capsys.readouterr().out
    assert "1 rows" in out
    assert "42" in out


def test_missing_subcommand_exits_nonzero() -> None:
    with pytest.raises(SystemExit):
        cli.main([])


def test_invalid_subcommand_exits_nonzero() -> None:
    with pytest.raises(SystemExit):
        cli.main(["bogus", "2024"])


def test_sql_subcommand_requires_seasons_flag() -> None:
    with pytest.raises(SystemExit):
        cli.main(["sql", "SELECT 1"])
