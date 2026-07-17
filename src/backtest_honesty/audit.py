from __future__ import annotations

from dataclasses import asdict, dataclass, field

import pandas as pd

from .chronology import ChronologyIssue, validate_trade_chronology


@dataclass(frozen=True)
class AuditConfig:
    require_entry_after_signal: bool = True
    reject_same_symbol_overlap: bool = True
    feature_time_columns: tuple[str, ...] = ()


@dataclass(frozen=True)
class AuditReport:
    rows: int
    passed: bool
    duplicate_trade_ids: int
    chronology_issues: tuple[ChronologyIssue, ...]
    overlap_count: int
    messages: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, object]:
        return {
            "rows": self.rows,
            "passed": self.passed,
            "duplicate_trade_ids": self.duplicate_trade_ids,
            "chronology_issues": [asdict(issue) for issue in self.chronology_issues],
            "overlap_count": self.overlap_count,
            "messages": list(self.messages),
        }


def _count_same_symbol_overlaps(trades: pd.DataFrame) -> int:
    required = {"symbol", "entry_time", "exit_time"}
    missing = required.difference(trades.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    work = trades.copy()
    work["entry_time"] = pd.to_datetime(work["entry_time"], errors="coerce", utc=True)
    work["exit_time"] = pd.to_datetime(work["exit_time"], errors="coerce", utc=True)

    overlaps = 0
    for _, group in work.sort_values(["symbol", "entry_time"]).groupby("symbol", sort=False):
        latest_exit = None
        for _, row in group.iterrows():
            if pd.isna(row["entry_time"]) or pd.isna(row["exit_time"]):
                continue
            if latest_exit is not None and row["entry_time"] < latest_exit:
                overlaps += 1
            latest_exit = row["exit_time"] if latest_exit is None else max(latest_exit, row["exit_time"])
    return overlaps


def audit_trade_ledger(trades: pd.DataFrame, config: AuditConfig | None = None) -> AuditReport:
    """Run strategy-agnostic chronology, duplication, and overlap checks."""
    config = config or AuditConfig()
    if "trade_id" not in trades.columns:
        raise ValueError("missing required column: trade_id")

    duplicate_trade_ids = int(trades["trade_id"].astype(str).duplicated().sum())
    chronology_issues = tuple(
        validate_trade_chronology(
            trades,
            require_entry_after_signal=config.require_entry_after_signal,
            feature_time_columns=config.feature_time_columns,
        )
    )
    overlap_count = _count_same_symbol_overlaps(trades) if config.reject_same_symbol_overlap else 0

    messages: list[str] = []
    if duplicate_trade_ids:
        messages.append(f"{duplicate_trade_ids} duplicate trade id(s)")
    if chronology_issues:
        messages.append(f"{len(chronology_issues)} chronology issue(s)")
    if overlap_count:
        messages.append(f"{overlap_count} same-symbol overlap(s)")
    if not messages:
        messages.append("all configured checks passed")

    return AuditReport(
        rows=len(trades),
        passed=not duplicate_trade_ids and not chronology_issues and not overlap_count,
        duplicate_trade_ids=duplicate_trade_ids,
        chronology_issues=chronology_issues,
        overlap_count=overlap_count,
        messages=tuple(messages),
    )
