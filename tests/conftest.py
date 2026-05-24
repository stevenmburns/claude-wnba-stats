"""Shared fixtures. Clears db._load's lru_cache around every test so that
patched loaders aren't bypassed by results cached from a prior test."""

import pytest

from claude_wnba_stats import db


@pytest.fixture(autouse=True)
def _clear_db_cache() -> None:
    db._load.cache_clear()
    yield
    db._load.cache_clear()
