"""Port for notification implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from web_scraping.application.dto.notification_result import NotificationResult


class NotificationGateway(ABC):
    """Define notification behavior for contract lookups."""

    @abstractmethod
    def send_lookup_notification(
        self,
        customer_name: str,
        city: str,
        contract_id: str,
    ) -> NotificationResult:
        """Send a simulated notification for a lookup request."""
