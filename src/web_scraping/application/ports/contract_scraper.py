"""Port for contract scraping implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from web_scraping.domain.entities.contract import Contract


class ContractScraper(ABC):
    """Define the contract lookup interface for scraping adapters."""

    @abstractmethod
    def fetch_contract(self, city: str, contract_id: str, mode: str) -> Contract:
        """Fetch contract data from an external source."""
