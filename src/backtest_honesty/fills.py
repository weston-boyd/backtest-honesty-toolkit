from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AmbiguousBarPolicy(str, Enum):
    """How to resolve a bar that touches both stop and target."""

    CONSERVATIVE = "conservative"
    OPTIMISTIC = "optimistic"
    REJECT = "reject"


@dataclass(frozen=True)
class FillResolution:
    exit_price: float | None
    reason: str
    ambiguous: bool
    accepted: bool


def resolve_bar_exit(
    *,
    side: str,
    bar_high: float,
    bar_low: float,
    stop_price: float,
    target_price: float,
    policy: AmbiguousBarPolicy = AmbiguousBarPolicy.CONSERVATIVE,
) -> FillResolution:
    """Resolve stop/target outcomes from OHLC-only information."""
    normalized_side = side.strip().lower()
    if normalized_side not in {"long", "short"}:
        raise ValueError("side must be 'long' or 'short'")
    if bar_high < bar_low:
        raise ValueError("bar_high must be >= bar_low")

    if normalized_side == "long":
        stop_hit = bar_low <= stop_price
        target_hit = bar_high >= target_price
    else:
        stop_hit = bar_high >= stop_price
        target_hit = bar_low <= target_price

    if stop_hit and target_hit:
        if policy is AmbiguousBarPolicy.REJECT:
            return FillResolution(None, "ambiguous_bar_rejected", True, False)
        if policy is AmbiguousBarPolicy.OPTIMISTIC:
            return FillResolution(target_price, "target_first_assumed", True, True)
        return FillResolution(stop_price, "stop_first_assumed", True, True)

    if stop_hit:
        return FillResolution(stop_price, "stop_hit", False, True)
    if target_hit:
        return FillResolution(target_price, "target_hit", False, True)
    return FillResolution(None, "no_exit", False, False)
