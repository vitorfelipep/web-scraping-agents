"""Tests for the contract lookup use case."""

from __future__ import annotations

from web_scraping.adapters.notifications.email_notification_simulator import (
    EmailNotificationSimulator,
)
from web_scraping.adapters.persistence.in_memory_contract_repository import (
    InMemoryContractRepository,
)
from web_scraping.adapters.scrapers.playwright_contract_scraper import (
    PlaywrightContractScraper,
)
from web_scraping.application.dto.contract_query import ContractQuery
from web_scraping.application.use_cases.fetch_contract_use_case import (
    FetchContractUseCase,
)
from web_scraping.settings import Settings


def test_fetch_contract_use_case_persists_and_notifies() -> None:
    """Validate the wiring of the initial hexagonal flow."""
    repository = InMemoryContractRepository()
    use_case = FetchContractUseCase(
        scraper=PlaywrightContractScraper(),
        repository=repository,
        notification_gateway=EmailNotificationSimulator(Settings()),
    )

    result = use_case.execute(
        ContractQuery(
            city="palmeira",
            contract_id="MV8yMDMy",
            mode="INFO",
            customer_name="Cliente X",
        )
    )

    assert result.contract.contract_id == "MV8yMDMy"
    assert result.contract.city == "palmeira"
    assert repository.get("MV8yMDMy") is not None
    assert result.notification.recipient == "vitorfelipep@dmmv-tech.com"
    assert result.persistence_mode == "in-memory"
