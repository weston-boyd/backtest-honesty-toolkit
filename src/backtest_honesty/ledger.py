from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class EquityReport:
    starting_equity: float
    ending_equity: float
    net_pnl: float
    max_drawdown_dollars: float
    max_drawdown_percent: float
    equity_curve: pd.DataFrame


def reconstruct_equity(
    trades: pd.DataFrame,
    *,
    starting_equity: float,
    pnl_column: str = "net_pnl",
    time_column: str = "exit_time",
) -> EquityReport:
    """Reconstruct equity chronologically from a closed-trade ledger."""
    if starting_equity <= 0:
        raise ValueError("starting_equity must be positive")
    missing = {pnl_column, time_column}.difference(trades.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    work = trades.copy()
    work[time_column] = pd.to_datetime(work[time_column], errors="coerce", utc=True)
    if work[time_column].isna().any():
        raise ValueError("ledger contains invalid exit timestamps")

    work = work.sort_values([time_column], kind="stable").reset_index(drop=True)
    work["pnl"] = pd.to_numeric(work[pnl_column], errors="raise")
    work["equity"] = starting_equity + work["pnl"].cumsum()
    work["peak_equity"] = work["equity"].cummax().clip(lower=starting_equity)
    work["drawdown_dollars"] = work["peak_equity"] - work["equity"]
    work["drawdown_percent"] = (
        work["drawdown_dollars"] / work["peak_equity"].replace(0, pd.NA) * 100.0
    ).fillna(0.0)

    ending_equity = float(work["equity"].iloc[-1]) if not work.empty else float(starting_equity)
    return EquityReport(
        starting_equity=float(starting_equity),
        ending_equity=ending_equity,
        net_pnl=ending_equity - float(starting_equity),
        max_drawdown_dollars=float(work["drawdown_dollars"].max()) if not work.empty else 0.0,
        max_drawdown_percent=float(work["drawdown_percent"].max()) if not work.empty else 0.0,
        equity_curve=work,
    )
