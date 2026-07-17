from backtest_honesty import AmbiguousBarPolicy, resolve_bar_exit


def test_conservative_ambiguous_long_bar_uses_stop():
    result = resolve_bar_exit(
        side="long",
        bar_high=110,
        bar_low=90,
        stop_price=95,
        target_price=105,
        policy=AmbiguousBarPolicy.CONSERVATIVE,
    )
    assert result.accepted is True
    assert result.ambiguous is True
    assert result.exit_price == 95
    assert result.reason == "stop_first_assumed"


def test_reject_policy_rejects_ambiguous_bar():
    result = resolve_bar_exit(
        side="short",
        bar_high=110,
        bar_low=90,
        stop_price=105,
        target_price=95,
        policy=AmbiguousBarPolicy.REJECT,
    )
    assert result.accepted is False
    assert result.exit_price is None
