from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CostModel:
    commission_per_side: float = 0.0
    slippage_per_side: float = 0.0

    def round_trip_cost(self, quantity: float) -> float:
        if quantity < 0:
            raise ValueError("quantity must be nonnegative")
        return quantity * 2.0 * (self.commission_per_side + self.slippage_per_side)


def apply_costs(
    trades: pd.DataFrame,
    model: CostModel,
    *,
    gross_pnl_column: str = "gross_pnl",
    quantity_column: str = "quantity",
) -> pd.DataFrame:
    """Return a copy with transaction costs and net PnL columns."""
    missing = {gross_pnl_column, quantity_column}.difference(trades.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")

    result = trades.copy()
    result["transaction_cost"] = result[quantity_column].astype(float).map(model.round_trip_cost)
    result["net_pnl"] = result[gross_pnl_column].astype(float) - result["transaction_cost"]
    return result
