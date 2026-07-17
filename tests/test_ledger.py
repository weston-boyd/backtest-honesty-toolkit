import pandas as pd

from backtest_honesty import reconstruct_equity


def test_reconstruct_equity_and_drawdown():
    trades = pd.DataFrame(
        {
            "exit_time": [
                "2026-01-01T10:00:00Z",
                "2026-01-01T11:00:00Z",
                "2026-01-01T12:00:00Z",
            ],
            "net_pnl": [100.0, -250.0, 200.0],
        }
    )
    report = reconstruct_equity(trades, starting_equity=1000.0)
    assert report.ending_equity == 1050.0
    assert report.net_pnl == 50.0
    assert report.max_drawdown_dollars == 250.0
