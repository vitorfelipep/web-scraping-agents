"""Contract item entity."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContractItem:
    """Represent one item from a public contract."""

    number: str
    denomination: str
    quantity: float
    unit_measure: str
    unit_value_brl: str
    total_value_brl: str
