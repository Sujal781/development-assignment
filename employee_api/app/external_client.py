"""
app/external_client.py

Handles all outbound HTTP calls to other APIs:
  - send_employee(): push a single employee record OUT to an external
    API endpoint
  - fetch_external_employees(): pull employee-like records IN from an
    external API and normalize them into this API's employee shape

Single Responsibility: this module only knows how to make HTTP calls
and reshape the responses. It has no idea Excel or FastAPI exist.
"""

from typing import List

import httpx

from app.config import EXTERNAL_FETCH_API_URL, EXTERNAL_SEND_API_URL


async def send_employee(employee: dict) -> dict:
    """POST a single employee record to the configured external endpoint
    and return whatever that endpoint responds with."""
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(EXTERNAL_SEND_API_URL, json=employee)
        response.raise_for_status()
        return response.json()


async def fetch_external_employees() -> List[dict]:
    """
    GET records from the configured external endpoint and normalize
    them into this API's employee shape (name, email, department,
    designation, salary).

    The default EXTERNAL_FETCH_API_URL points at jsonplaceholder's
    /users endpoint, so the normalization below is written for that
    response shape: [{id, name, email, address, phone, company:{name}}, ...].
    If you point this at a different API, adjust the mapping below to
    match its actual response shape.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(EXTERNAL_FETCH_API_URL)
        response.raise_for_status()
        raw_records = response.json()

    normalized = []
    for raw in raw_records:
        company = raw.get("company") or {}
        normalized.append({
            "name": raw.get("name", "Unknown"),
            "email": raw.get("email", f"unknown{raw.get('id', '0')}@example.com"),
            "department": "Imported",
            "designation": company.get("name", "N/A"),
            "salary": 0.0,
        })
    return normalized
