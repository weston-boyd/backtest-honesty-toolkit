import pandas as pd

from backtest_honesty import AuditConfig, audit_trade_ledger


def valid_trades() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "trade_id": ["T1", "T2"],
            "symbol": ["AAA", "AAA"],
            "side": ["long", "long"],
            "signal_time": ["2026-01-01T09:30:00Z", "2026-01-01T10:00:00Z"],
            "entry_time": ["2026-01-01T09:31:00Z", "2026-01-01T10:01:00Z"],
            "exit_time": ["2026-01-01T09:50:00Z", "2026-01-01T10:20:00Z"],
            "entry_price": [100.0, 101.0],
            "exit_price": [102.0, 103.0],
            "quantity": [1, 1],
        }
    )


def test_clean_ledger_passes():
    report = audit_trade_ledger(valid_trades(), AuditConfig())
    assert report.passed is True


def test_duplicate_id_and_overlap_fail():
    trades = valid_trades()
    trades.loc[1, "trade_id"] = "T1"
    trades.loc[1, "entry_time"] = "2026-01-01T09:40:00Z"
    report = audit_trade_ledger(trades)
    assert report.passed is False
    assert report.duplicate_trade_ids == 1
    assert report.overlap_count == 1
