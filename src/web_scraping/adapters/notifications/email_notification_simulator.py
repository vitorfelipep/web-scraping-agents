"""Simulated email notification adapter."""

from __future__ import annotations

from datetime import UTC, datetime

from web_scraping.application.dto.notification_result import NotificationResult
from web_scraping.ports.notification_gateway import NotificationGateway
from web_scraping.settings import Settings


class EmailNotificationSimulator(NotificationGateway):
    """Simulate an email dispatch for lookup requests."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def send_lookup_notification(
        self,
        customer_name: str,
        city: str,
        contract_id: str,
    ) -> NotificationResult:
        """Return a simulated email receipt without external side effects."""
        subject = f"Consulta de contrato {contract_id} para {city}"
        description = f"Solicitacao executada por {customer_name}."
        return NotificationResult(
            status=f"simulated: {description}",
            recipient=self._settings.notification_recipient,
            subject=subject,
            sent_at=datetime.now(UTC).isoformat(),
        )
