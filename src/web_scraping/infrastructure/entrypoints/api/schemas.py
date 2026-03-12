"""HTTP schemas for the contract API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ContractQueryParams(BaseModel):
    """Represent the query string expected by the API."""

    id: str = Field(..., description="Portal contract identifier.")
    mode: str = Field(default="INFO", description="Portal contract mode.")
    customer_name: str = Field(
        default="cliente-x",
        description="Customer responsible for the request.",
    )


class HealthResponse(BaseModel):
    """Represent a minimal health response."""

    status: str
