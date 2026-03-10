"""Port for contract persistence implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from web_scraping.domain.entities.contract import Contract


class ContractRepository(ABC):
    """Define contract persistence behavior."""

    @property
    @abstractmethod
    def storage_mode(self) -> str:
        """Return the human-readable storage mode."""

    @abstractmethod
    def save(self, contract: Contract) -> None:
        """Persist one contract."""
