"""DTO for contract lookup output."""

from __future__ import annotations

from dataclasses import dataclass

from web_scraping.application.dto.notification_result import NotificationResult
from web_scraping.domain.entities.contract import Contract


@dataclass(frozen=True)
class ContractLookupResult:
    """Combine fetched contract data with persistence and notification metadata."""

    contract: Contract
    persistence_mode: str
    notification: NotificationResult
