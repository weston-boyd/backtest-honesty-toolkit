import pandas as pd

from backtest_honesty import validate_trade_chronology


def test_next_bar_entry_passes():
    trades = pd.DataFrame(
        {
            "trade_id": ["T1"],
            "signal_time": ["2026-01-01T09:30:00Z"],
            "entry_time": ["2026-01-01T09:31:00Z"],
            "exit_time": ["2026-01-01T09:40:00Z"],
            "feature_time": ["2026-01-01T09:29:00Z"],
        }
    )
    issues = validate_trade_chronology(trades, feature_time_columns=("feature_time",))
    assert issues == []


def test_same_bar_entry_is_flagged():
    trades = pd.DataFrame(
        {
            "trade_id": ["T1"],
            "signal_time": ["2026-01-01T09:30:00Z"],
            "entry_time": ["2026-01-01T09:30:00Z"],
            "exit_time": ["2026-01-01T09:40:00Z"],
        }
    )
    issues = validate_trade_chronology(trades)
    assert any(issue.code == "entry_not_after_signal" for issue in issues)


def test_future_feature_is_flagged():
    trades = pd.DataFrame(
        {
            "trade_id": ["T1"],
            "signal_time": ["2026-01-01T09:30:00Z"],
            "entry_time": ["2026-01-01T09:31:00Z"],
            "exit_time": ["2026-01-01T09:40:00Z"],
            "feature_time": ["2026-01-01T09:30:01Z"],
        }
    )
    issues = validate_trade_chronology(trades, feature_time_columns=("feature_time",))
    assert any(issue.code == "feature_lookahead" for issue in issues)
