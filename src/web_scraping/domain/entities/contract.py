"""Contract aggregate entity."""

from __future__ import annotations

from dataclasses import dataclass, field

from web_scraping.domain.entities.contract_item import ContractItem


@dataclass(frozen=True)
class Contract:
    """Represent the contract data collected from the transparency portal."""

    city: str
    contract_id: str
    municipality_name: str
    total_value_brl: str
    description: str
    signature_date: str
    start_date: str
    expiration_date: str
    supplier: str
    branch: str
    bid_reference: str
    legal_responsibles: list[str] = field(default_factory=list)
    managers: list[str] = field(default_factory=list)
    inspectors: list[str] = field(default_factory=list)
    items: list[ContractItem] = field(default_factory=list)
