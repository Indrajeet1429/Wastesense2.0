"""API tests for the WASTESENSE FastAPI application."""

import asyncio

import httpx

from backend.main import app


def request(
    method: str,
    path: str,
    json: dict | None = None,
) -> httpx.Response:
    """Send an HTTP request through the ASGI application."""

    async def make_request() -> httpx.Response:
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            return await client.request(method, path, json=json)

    return asyncio.run(make_request())


def test_root_endpoint() -> None:
    """Check that the root endpoint reports a healthy application."""
    response = request("GET", "/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_health_endpoint() -> None:
    """Check that the API health endpoint reports healthy status."""
    response = request("GET", "/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_openapi_contains_shared_routes() -> None:
    """Check that all agreed API routes are registered."""
    paths = app.openapi()["paths"]

    expected_paths = {
        "/api/overview",
        "/api/machines",
        "/api/machines/{machine_id}",
        "/api/workloads",
        "/api/waste",
        "/api/waste/{waste_id}",
        "/api/alerts",
        "/api/trends",
        "/api/savings",
        "/api/replay/{waste_id}",
        "/api/optimization",
        "/api/waste/analyze",
    }

    assert expected_paths.issubset(paths.keys())


def test_unintegrated_overview_returns_501() -> None:
    """Check that the overview endpoint clearly reports pending integration."""
    response = request("GET", "/api/overview")

    assert response.status_code == 501


def test_analyze_rejects_missing_required_fields() -> None:
    """Check that an empty analysis request fails validation."""
    response = request("POST", "/api/waste/analyze")

    assert response.status_code == 422


def test_analyze_rejects_invalid_cpu_capacity() -> None:
    """Check that zero CPU capacity fails request validation."""
    payload = {
        "machine_id": "M102",
        "timestamp": "2026-10-10T14:30:00",
        "active_tasks": 5,
        "workload_type": "COMPUTE",
        "cpu_capacity": 0,
        "memory_capacity": 16,
        "actual_cpu": 40,
        "actual_memory": 8,
    }

    response = request(
        "POST",
        "/api/waste/analyze",
        json=payload,
    )

    assert response.status_code == 422