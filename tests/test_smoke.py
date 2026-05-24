"""Sanity check that the package imports."""

from claude_wnba_stats import __version__


def test_version() -> None:
    assert __version__ == "0.1.0"
