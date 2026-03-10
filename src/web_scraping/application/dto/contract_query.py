"""DTO for contract lookup input."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ContractQuery:
    """Represent the incoming request for a contract lookup."""

    city: str
    contract_id: str
    mode: str
    customer_name: str
