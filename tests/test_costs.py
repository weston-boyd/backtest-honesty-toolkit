import pandas as pd

from backtest_honesty import CostModel, apply_costs


def test_cost_model_applies_round_trip_costs():
    trades = pd.DataFrame({"gross_pnl": [100.0], "quantity": [2]})
    result = apply_costs(
        trades,
        CostModel(commission_per_side=1.0, slippage_per_side=0.5),
    )
    assert result.iloc[0]["transaction_cost"] == 6.0
    assert result.iloc[0]["net_pnl"] == 94.0
