"""Tiny CLI: `wnba-stats schedule 2024` prints the first rows."""

from __future__ import annotations

import argparse
import sys

from . import data, db


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="wnba-stats")
    sub = parser.add_subparsers(dest="cmd", required=True)

    for name in ("schedule", "team-boxscores", "player-boxscores"):
        p = sub.add_parser(name)
        p.add_argument("seasons", nargs="+", type=int, help="One or more seasons, e.g. 2023 2024")
        p.add_argument("--head", type=int, default=10, help="Rows to print (default 10)")

    sql_p = sub.add_parser("sql", help="Run a DuckDB SQL query against the loaded WNBA tables")
    sql_p.add_argument(
        "query", help="SQL string; tables: schedule, team_boxscores, player_boxscores"
    )
    sql_p.add_argument("--seasons", nargs="+", type=int, required=True)
    sql_p.add_argument("--head", type=int, default=20, help="Rows to print (default 20)")

    args = parser.parse_args(argv)

    if args.cmd == "sql":
        df = db.query(args.query, args.seasons)
        print(f"{len(df):,} rows, {len(df.columns)} columns")
        print(df.head(args.head).to_string(index=False))
        return 0

    fn = {
        "schedule": data.schedule,
        "team-boxscores": data.team_boxscores,
        "player-boxscores": data.player_boxscores,
    }[args.cmd]

    df = fn(args.seasons)
    print(f"{len(df):,} rows, {len(df.columns)} columns")
    print(df.head(args.head).to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
