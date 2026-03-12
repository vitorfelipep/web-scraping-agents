"""Use case for fetching, storing and notifying a contract lookup."""

from __future__ import annotations

from web_scraping.application.dto.contract_lookup_result import ContractLookupResult
from web_scraping.application.dto.contract_query import ContractQuery
from web_scraping.application.ports.contract_repository import ContractRepository
from web_scraping.application.ports.contract_scraper import ContractScraper
from web_scraping.application.ports.notification_gateway import NotificationGateway


class FetchContractUseCase:
    """Coordinate the contract lookup workflow."""

    def __init__(
        self,
        scraper: ContractScraper,
        repository: ContractRepository,
        notification_gateway: NotificationGateway,
    ) -> None:
        self._scraper = scraper
        self._repository = repository
        self._notification_gateway = notification_gateway

    def execute(self, query: ContractQuery) -> ContractLookupResult:
        """Fetch a contract, persist it and simulate notification dispatch."""
        contract = self._scraper.fetch_contract(
            city=query.city,
            contract_id=query.contract_id,
            mode=query.mode,
        )
        self._repository.save(contract)
        notification = self._notification_gateway.send_lookup_notification(
            customer_name=query.customer_name,
            city=query.city,
            contract_id=query.contract_id,
        )
        return ContractLookupResult(
            contract=contract,
            persistence_mode=self._repository.storage_mode,
            notification=notification,
        )
