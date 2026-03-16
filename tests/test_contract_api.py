"""HTTP tests for the contract API entrypoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from web_scraping.infrastructure.entrypoints.api.app import app


def test_get_contract_accepts_query_params() -> None:
    """Validate the GET endpoint contract using query string parameters."""
    client = TestClient(app)

    response = client.get(
        "/contracts/palmeira",
        params={
            "id": "MV8yMDMy",
            "mode": "INFO",
            "customer_name": "Cliente X",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["request"]["city"] == "palmeira"
    assert payload["request"]["params"]["id"] == "MV8yMDMy"
    assert payload["request"]["params"]["mode"] == "INFO"
    assert payload["request"]["customer_name"] == "Cliente X"
    assert payload["contract"]["municipality_name"] == "Prefeitura Municipal de Palmeira"
    assert payload["notification"]["recipient"] == "vitorfelipep@dmmv-tech.com"


def test_get_contract_requires_contract_id() -> None:
    """Validate FastAPI returns an error when required query params are missing."""
    client = TestClient(app)

    response = client.get(
        "/contracts/palmeira",
        params={
            "mode": "INFO",
            "customer_name": "Cliente X",
        },
    )

    assert response.status_code == 422
