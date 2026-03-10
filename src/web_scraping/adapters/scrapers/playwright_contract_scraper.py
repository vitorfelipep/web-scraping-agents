"""Playwright scraper adapter placeholder."""

from __future__ import annotations

from web_scraping.domain.entities.contract import Contract
from web_scraping.domain.entities.contract_item import ContractItem
from web_scraping.ports.contract_scraper import ContractScraper


class PlaywrightContractScraper(ContractScraper):
    """Provide a temporary scraper stub until the real portal integration lands."""

    def fetch_contract(self, city: str, contract_id: str, mode: str) -> Contract:
        """Return a deterministic placeholder contract for local integration wiring."""
        return Contract(
            city=city,
            contract_id=contract_id,
            municipality_name="Prefeitura Municipal de Palmeira",
            total_value_brl="R$ 0,00",
            description=f"Stub inicial para contrato {contract_id} em modo {mode}",
            signature_date="",
            start_date="",
            expiration_date="",
            supplier="",
            branch="",
            bid_reference="",
            legal_responsibles=[],
            managers=[],
            inspectors=[],
            items=[
                ContractItem(
                    number="1",
                    denomination="Item inicial",
                    quantity=0.0,
                    unit_measure="UN",
                    unit_value_brl="R$ 0,00",
                    total_value_brl="R$ 0,00",
                )
            ],
        )
