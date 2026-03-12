"""FastAPI application factory."""

from __future__ import annotations

from fastapi import FastAPI

from web_scraping.application.dto.contract_query import ContractQuery
from web_scraping.application.use_cases.fetch_contract_use_case import (
    FetchContractUseCase,
)
from web_scraping.infrastructure.config.settings import Settings
from web_scraping.infrastructure.entrypoints.api.schemas import (
    ContractQueryParams,
    HealthResponse,
)
from web_scraping.infrastructure.notifications.email_notification_simulator import (
    EmailNotificationSimulator,
)
from web_scraping.infrastructure.persistence.in_memory_contract_repository import (
    InMemoryContractRepository,
)
from web_scraping.infrastructure.scraping.playwright_contract_scraper import (
    PlaywrightContractScraper,
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    runtime_settings = settings or Settings()
    app = FastAPI(title=runtime_settings.api_title, version=runtime_settings.api_version)
    use_case = FetchContractUseCase(
        scraper=PlaywrightContractScraper(),
        repository=InMemoryContractRepository(),
        notification_gateway=EmailNotificationSimulator(runtime_settings),
    )

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        """Expose a minimal health endpoint."""
        return HealthResponse(status="ok")

    @app.get("/contracts/{city}")
    def get_contract(city: str, params: ContractQueryParams) -> dict[str, object]:
        """Return a JSON payload for one contract lookup."""
        result = use_case.execute(
            ContractQuery(
                city=city,
                contract_id=params.id,
                mode=params.mode,
                customer_name=params.customer_name,
            )
        )
        contract = result.contract
        return {
            "request": {
                "city": city,
                "params": {
                    "id": params.id,
                    "mode": params.mode,
                },
                "customer_name": params.customer_name,
            },
            "contract": {
                "municipality_name": contract.municipality_name,
                "total_value_brl": contract.total_value_brl,
                "description": contract.description,
                "signature_date": contract.signature_date,
                "start_date": contract.start_date,
                "expiration_date": contract.expiration_date,
                "supplier": contract.supplier,
                "branch": contract.branch,
                "bid_reference": contract.bid_reference,
                "legal_responsibles": contract.legal_responsibles,
                "managers": contract.managers,
                "inspectors": contract.inspectors,
                "items": [
                    {
                        "number": item.number,
                        "denomination": item.denomination,
                        "quantity": item.quantity,
                        "unit_measure": item.unit_measure,
                        "unit_value_brl": item.unit_value_brl,
                        "total_value_brl": item.total_value_brl,
                    }
                    for item in contract.items
                ],
            },
            "persistence": {
                "mode": result.persistence_mode,
            },
            "notification": {
                "status": result.notification.status,
                "recipient": result.notification.recipient,
                "subject": result.notification.subject,
                "sent_at": result.notification.sent_at,
            },
        }

    return app


app = create_app()
