"""Smoke test: package imports and exposes the public API."""

from claude_wnba_stats import __version__, data, db


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_public_api() -> None:
    assert callable(data.schedule)
    assert callable(data.team_boxscores)
    assert callable(data.player_boxscores)
    assert callable(db.connect)
    assert callable(db.query)
