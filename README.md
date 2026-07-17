# Backtest Honesty Toolkit

A tested Python toolkit for detecting common sources of optimism, leakage, and execution ambiguity in systematic-trading research.

This public project is adapted from reusable validation practices developed for **WesB Algos**. It contains generic research-audit infrastructure only. It does **not** include proprietary strategies, entry thresholds, symbol-selection logic, broker credentials, or deployment code.

## Implemented Checks

- Signal/entry chronology validation
- Next-bar-entry enforcement
- Feature timestamp leakage checks
- Duplicate trade detection
- Same-symbol overlap detection
- Exit-before-entry detection
- Ledger ordering checks
- Conservative ambiguous-bar fill resolution
- Execution-cost application
- Equity and drawdown reconstruction
- Serializable audit summaries
- Automated pytest coverage
- GitHub Actions continuous integration

## Why This Exists

A backtest can look excellent while still relying on:

- same-bar entries after observing the close;
- features calculated with future information;
- overlapping positions that the live system would reject;
- optimistic assumptions when both stop and target are touched in one bar;
- omitted fees and slippage;
- unordered or duplicated trade records.

This toolkit makes those assumptions explicit and testable.

## Project Structure

```text
backtest-honesty-toolkit/
├── src/backtest_honesty/
│   ├── chronology.py
│   ├── fills.py
│   ├── ledger.py
│   ├── costs.py
│   └── audit.py
├── tests/
├── examples/
├── docs/
└── pyproject.toml
```

## Installation

```bash
git clone https://github.com/weston-boyd/backtest-honesty-toolkit.git
cd backtest-honesty-toolkit
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run Tests

```bash
pytest
```

## Run Example

```bash
python examples/audit_example.py
```

## Quick Example

```python
import pandas as pd

from backtest_honesty import AuditConfig, audit_trade_ledger

trades = pd.DataFrame(
    {
        "trade_id": ["T1"],
        "symbol": ["DEMO"],
        "side": ["long"],
        "signal_time": ["2026-01-01T09:30:00Z"],
        "entry_time": ["2026-01-01T09:31:00Z"],
        "exit_time": ["2026-01-01T09:40:00Z"],
        "entry_price": [100.0],
        "exit_price": [102.0],
        "quantity": [1],
    }
)

report = audit_trade_ledger(
    trades,
    AuditConfig(
        require_entry_after_signal=True,
        reject_same_symbol_overlap=True,
    ),
)

print(report.to_dict())
```

## Design Goals

- Conservative defaults
- Explicit assumptions
- Deterministic outputs
- Serializable reports
- Strategy-agnostic APIs
- No dependency on a specific broker or platform

## License

MIT License
