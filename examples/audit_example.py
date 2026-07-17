import json

import pandas as pd

from backtest_honesty import (
    AuditConfig,
    CostModel,
    apply_costs,
    audit_trade_ledger,
    reconstruct_equity,
)


def main() -> None:
    trades = pd.DataFrame(
        {
            "trade_id": ["T1", "T2"],
            "symbol": ["DEMO", "DEMO"],
            "side": ["long", "short"],
            "signal_time": ["2026-01-01T09:30:00Z", "2026-01-01T10:00:00Z"],
            "entry_time": ["2026-01-01T09:31:00Z", "2026-01-01T10:01:00Z"],
            "exit_time": ["2026-01-01T09:45:00Z", "2026-01-01T10:20:00Z"],
            "entry_price": [100.0, 102.0],
            "exit_price": [103.0, 100.0],
            "quantity": [1, 1],
            "gross_pnl": [300.0, 200.0],
        }
    )

    audit = audit_trade_ledger(trades, AuditConfig())
    costed = apply_costs(
        trades,
        CostModel(commission_per_side=1.25, slippage_per_side=0.75),
    )
    equity = reconstruct_equity(costed, starting_equity=10_000.0)

    print("Audit:")
    print(json.dumps(audit.to_dict(), indent=2))
    print("\nEnding equity:", equity.ending_equity)
    print("Max drawdown %:", round(equity.max_drawdown_percent, 4))


if __name__ == "__main__":
    main()
