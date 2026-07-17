from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class ChronologyIssue:
    row_index: int
    trade_id: str
    code: str
    message: str


def _utc_series(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce", utc=True)


def validate_trade_chronology(
    trades: pd.DataFrame,
    *,
    require_entry_after_signal: bool = True,
    feature_time_columns: Iterable[str] = (),
) -> list[ChronologyIssue]:
    """Validate trade timestamps without mutating the input."""
    required = {"trade_id", "signal_time", "entry_time", "exit_time"}
    missing = required.difference(trades.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    work = trades.copy()
    for column in ("signal_time", "entry_time", "exit_time", *feature_time_columns):
        if column not in work.columns:
            raise ValueError(f"missing timestamp column: {column}")
        work[column] = _utc_series(work[column])

    issues: list[ChronologyIssue] = []
    for index, row in work.iterrows():
        trade_id = str(row["trade_id"])

        if pd.isna(row["signal_time"]) or pd.isna(row["entry_time"]) or pd.isna(row["exit_time"]):
            issues.append(
                ChronologyIssue(int(index), trade_id, "invalid_timestamp", "one or more timestamps are invalid")
            )
            continue

        if require_entry_after_signal and row["entry_time"] <= row["signal_time"]:
            issues.append(
                ChronologyIssue(
                    int(index),
                    trade_id,
                    "entry_not_after_signal",
                    "entry_time must be strictly later than signal_time",
                )
            )

        if row["exit_time"] < row["entry_time"]:
            issues.append(
                ChronologyIssue(
                    int(index),
                    trade_id,
                    "exit_before_entry",
                    "exit_time cannot be earlier than entry_time",
                )
            )

        for column in feature_time_columns:
            if pd.isna(row[column]):
                issues.append(
                    ChronologyIssue(int(index), trade_id, "invalid_feature_time", f"{column} is invalid")
                )
            elif row[column] > row["signal_time"]:
                issues.append(
                    ChronologyIssue(
                        int(index),
                        trade_id,
                        "feature_lookahead",
                        f"{column} occurs after signal_time",
                    )
                )

    return issues
