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

text
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


## Installation

bash
git clone https://github.com/weston-boyd/backtest-honesty-toolkit.git
cd backtest-honesty-toolkit
python -m venv .venv


Windows PowerShell:

powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"


## Run Tests

bash
pytest


## Run Example

bash
python examples/audit_example.py


## Quick Example

python
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


## Design Goals

- Conservative defaults
- Explicit assumptions
- Deterministic outputs
- Serializable reports
- Strategy-agnostic APIs
- No dependency on a specific broker or platform

## License

MIT License

README_Backtest_Honesty_Toolkit.md

Replace the current README.md contents with this file, then commit with:

Improve README positioning, examples, and project scope



Library
/
README_Backtest_Honesty_Toolkit.md


# Backtest Honesty Toolkit

[![Tests](https://github.com/weston-boyd/backtest-honesty-toolkit/actions/workflows/python-app.yml/badge.svg)](https://github.com/weston-boyd/backtest-honesty-toolkit/actions/workflows/python-app.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A tested Python toolkit for detecting hidden optimism, timestamp leakage, execution ambiguity, and ledger inconsistencies in systematic-trading research.

This repository contains reusable research-validation components extracted from the private **WesB Algos** platform. It includes only generic audit infrastructure; no proprietary strategies, signal thresholds, symbol-selection logic, broker integrations, deployment code, or research datasets are included.

## Implemented Checks

- Signal and entry chronology validation
- Next-bar-entry enforcement
- Feature timestamp leakage detection
- Duplicate trade detection
- Same-symbol overlap detection
- Exit-before-entry detection
- Ledger ordering checks
- Conservative ambiguous-bar fill resolution
- Explicit execution-cost application
- Equity and drawdown reconstruction
- Serializable audit summaries
- Automated pytest coverage
- GitHub Actions continuous integration

## Why This Exists

A backtest can appear profitable while still depending on unrealistic or invalid assumptions, including:

- entering on the same bar after observing its close;
- calculating features with future information;
- allowing overlapping positions that a live system would reject;
- assuming a favorable outcome when both stop and target are touched in one bar;
- omitting commissions and slippage;
- using unordered or duplicated trade records.

Backtest Honesty Toolkit makes these assumptions explicit, testable, and reproducible.

## Project Structure

```text
backtest-honesty-toolkit/
├── src/
│   └── backtest_honesty/
│       ├── __init__.py
│       ├── audit.py
│       ├── chronology.py
│       ├── costs.py
│       ├── fills.py
│       └── ledger.py
├── tests/
├── examples/
├── docs/
├── LICENSE
├── README.md
└── pyproject.toml
```

## Installation

Clone the repository and create a virtual environment:

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

### macOS or Linux

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run Tests

```bash
pytest
```

## Run the Example

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

Example output:

```python
{
    "rows": 1,
    "passed": True,
    "duplicate_trade_ids": 0,
    "chronology_issues": [],
    "overlap_count": 0,
    "messages": ["all configured checks passed"],
}
```

## Design Goals

- Conservative defaults
- Explicit assumptions
- Deterministic behavior
- Serializable reports
- Strategy-agnostic APIs
- Broker-independent validation
- Clear separation between public infrastructure and proprietary research

## Scope

This toolkit is designed to audit generic research and backtest records. It does not attempt to determine whether a trading strategy is profitable, robust, or suitable for live deployment.

It also does not include:

- strategy entry or exit logic;
- optimization parameters;
- alpha models;
- portfolio-selection rules;
- broker credentials;
- live order submission;
- proprietary datasets or research results.

## License

Released under the [MIT License](LICENSE).
Library
/
README_Backtest_Honesty_Toolkit.md


# Backtest Honesty Toolkit

[![Tests](https://github.com/weston-boyd/backtest-honesty-toolkit/actions/workflows/python-app.yml/badge.svg)](https://github.com/weston-boyd/backtest-honesty-toolkit/actions/workflows/python-app.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A tested Python toolkit for detecting hidden optimism, timestamp leakage, execution ambiguity, and ledger inconsistencies in systematic-trading research.

This repository contains reusable research-validation components extracted from the private **WesB Algos** platform. It includes only generic audit infrastructure; no proprietary strategies, signal thresholds, symbol-selection logic, broker integrations, deployment code, or research datasets are included.

## Implemented Checks

- Signal and entry chronology validation
- Next-bar-entry enforcement
- Feature timestamp leakage detection
- Duplicate trade detection
- Same-symbol overlap detection
- Exit-before-entry detection
- Ledger ordering checks
- Conservative ambiguous-bar fill resolution
- Explicit execution-cost application
- Equity and drawdown reconstruction
- Serializable audit summaries
- Automated pytest coverage
- GitHub Actions continuous integration

## Why This Exists

A backtest can appear profitable while still depending on unrealistic or invalid assumptions, including:

- entering on the same bar after observing its close;
- calculating features with future information;
- allowing overlapping positions that a live system would reject;
- assuming a favorable outcome when both stop and target are touched in one bar;
- omitting commissions and slippage;
- using unordered or duplicated trade records.

Backtest Honesty Toolkit makes these assumptions explicit, testable, and reproducible.

## Project Structure

```text
backtest-honesty-toolkit/
├── src/
│   └── backtest_honesty/
│       ├── __init__.py
│       ├── audit.py
│       ├── chronology.py
│       ├── costs.py
│       ├── fills.py
│       └── ledger.py
├── tests/
├── examples/
├── docs/
├── LICENSE
├── README.md
└── pyproject.toml
```

## Installation

Clone the repository and create a virtual environment:

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

### macOS or Linux

```bash
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run Tests

```bash
pytest
```

## Run the Example

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

Example output:

```python
{
    "rows": 1,
    "passed": True,
    "duplicate_trade_ids": 0,
    "chronology_issues": [],
    "overlap_count": 0,
    "messages": ["all configured checks passed"],
}
```

## Design Goals

- Conservative defaults
- Explicit assumptions
- Deterministic behavior
- Serializable reports
- Strategy-agnostic APIs
- Broker-independent validation
- Clear separation between public infrastructure and proprietary research

## Scope

This toolkit is designed to audit generic research and backtest records. It does not attempt to determine whether a trading strategy is profitable, robust, or suitable for live deployment.

It also does not include:

- strategy entry or exit logic;
- optimization parameters;
- alpha models;
- portfolio-selection rules;
- broker credentials;
- live order submission;
- proprietary datasets or research results.

## License

Released under the [MIT License](LICENSE).
