# Backtest Honesty Toolkit

![Tests](https://img.shields.io/badge/Tests-Passing-success)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A tested Python toolkit for detecting hidden optimism, timestamp leakage, execution ambiguity, and ledger inconsistencies in systematic trading research.

---

## Overview

Backtest Honesty Toolkit contains reusable research-validation components extracted from the private **WesB Algos** research platform.

The repository includes only generic validation infrastructure.

It **does not** include:

- Proprietary trading strategies
- Alpha models
- Signal thresholds
- Symbol-selection logic
- Broker integrations
- Deployment code
- Research datasets

The goal is to help systematic traders build backtests that are honest, reproducible, and suitable for real-world validation.

---

# Implemented Checks

- Signal and entry chronology validation
- Next-bar entry enforcement
- Feature timestamp leakage detection
- Duplicate trade detection
- Same-symbol overlap detection
- Exit-before-entry detection
- Ledger ordering validation
- Conservative ambiguous-bar fill resolution
- Explicit commission and slippage application
- Equity reconstruction
- Drawdown reconstruction
- Serializable audit summaries
- Automated pytest coverage
- GitHub Actions CI

---

# Why This Exists

Many profitable-looking backtests unknowingly rely on optimistic assumptions such as:

- entering after observing the current bar
- future-data leakage
- overlapping positions
- optimistic stop/target fills
- missing commissions
- missing slippage
- unordered trade ledgers

This toolkit makes those assumptions explicit and automatically testable.

---

# Project Structure

```
backtest-honesty-toolkit/
│
├── src/
│   └── backtest_honesty/
│       ├── audit.py
│       ├── chronology.py
│       ├── costs.py
│       ├── fills.py
│       └── ledger.py
│
├── tests/
├── examples/
├── docs/
├── LICENSE
├── README.md
└── pyproject.toml
```

---

# Installation

```bash
git clone https://github.com/weston-boyd/backtest-honesty-toolkit.git

cd backtest-honesty-toolkit

python -m venv .venv
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

python -m pip install -e ".[dev]"
```

### macOS / Linux

```bash
source .venv/bin/activate

python -m pip install --upgrade pip

python -m pip install -e ".[dev]"
```

---

# Running Tests

```bash
pytest
```

---

# Example

```python
import pandas as pd

from backtest_honesty import AuditConfig
from backtest_honesty import audit_trade_ledger

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

---

# Design Goals

- Conservative defaults
- Explicit assumptions
- Deterministic behavior
- Serializable reports
- Strategy-agnostic APIs
- Broker-independent validation

---

# Scope

This toolkit audits the integrity of research and backtest records.

It is **not** intended to:

- determine whether a strategy is profitable
- optimize strategies
- generate alpha
- select portfolios
- submit live orders
- connect to brokers

---

# License

Released under the MIT License.
