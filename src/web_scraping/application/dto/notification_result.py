"""DTO for simulated notification output."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationResult:
    """Represent a simulated notification delivery."""

    status: str
    recipient: str
    subject: str
    sent_at: str
