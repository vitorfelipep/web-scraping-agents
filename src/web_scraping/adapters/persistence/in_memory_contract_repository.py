"""In-memory repository adapter for contracts."""

from __future__ import annotations

from web_scraping.domain.entities.contract import Contract
from web_scraping.ports.contract_repository import ContractRepository


class InMemoryContractRepository(ContractRepository):
    """Persist contracts in memory for local validation."""

    def __init__(self) -> None:
        self._contracts: dict[str, Contract] = {}

    @property
    def storage_mode(self) -> str:
        """Return the configured storage mode."""
        return "in-memory"

    def save(self, contract: Contract) -> None:
        """Persist a contract in the local memory store."""
        self._contracts[contract.contract_id] = contract

    def get(self, contract_id: str) -> Contract | None:
        """Return a previously stored contract if present."""
        return self._contracts.get(contract_id)
