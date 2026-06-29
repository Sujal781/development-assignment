"""
app/main.py

FastAPI application exposing CRUD endpoints for employee records
stored in an Excel file, plus two external-integration endpoints.

Like app.py in the customer demo, this file only orchestrates - it
calls into ExcelEmployeeStore and external_client to do the actual
work, and contains no business logic of its own.

Run with (from the employee_api/ folder):
    uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs for interactive API docs.
"""

from typing import List

from fastapi import FastAPI, HTTPException

from app.config import EXCEL_FILE_PATH
from app.excel_store import ExcelEmployeeStore
from app.external_client import fetch_external_employees, send_employee
from app.models import Employee, EmployeeCreate, EmployeeUpdate

app = FastAPI(
    title="Employee Records API",
    description="A FastAPI service that stores employee records in an Excel file.",
    version="1.0.0",
)

store = ExcelEmployeeStore(EXCEL_FILE_PATH)


@app.get("/")
def root():
    return {"message": "Employee Records API is running. See /docs for usage."}


# ---------------------------------------------------------------------------
# CRUD endpoints - read, create, update, delete
# ---------------------------------------------------------------------------

@app.get("/employees", response_model=List[Employee])
def list_employees():
    """Read all employee records from the Excel file."""
    return store.get_all()


@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: str):
    """Read a single employee record by ID."""
    record = store.get_by_id(employee_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return record


@app.post("/employees", response_model=Employee, status_code=201)
def create_employee(employee: EmployeeCreate):
    """Create a new employee record and append it to the Excel file."""
    return store.create(employee.model_dump())


@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: str, employee: EmployeeUpdate):
    """Update one or more fields of an existing employee record."""
    updated = store.update(employee_id, employee.model_dump(exclude_unset=True))
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    return updated


@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: str):
    """Delete an employee record from the Excel file."""
    deleted = store.delete(employee_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")


# ---------------------------------------------------------------------------
# External integration endpoints
# ---------------------------------------------------------------------------

@app.post("/employees/{employee_id}/send")
async def send_employee_to_external_api(employee_id: str):
    """Send a single employee's record to the configured external API
    (EXTERNAL_SEND_API_URL in app/config.py)."""
    record = store.get_by_id(employee_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Employee {employee_id} not found")
    external_response = await send_employee(record)
    return {"sent": record, "external_response": external_response}


@app.post("/employees/sync-external")
async def sync_from_external_api():
    """
    Pull records from the configured external API
    (EXTERNAL_FETCH_API_URL in app/config.py) and upsert them into the
    Excel database, matching on email - the same reuse-or-generate
    identity logic as the customer demo's GCID resolution, just keyed
    on email instead of producing a GCID.
    """
    incoming = await fetch_external_employees()
    created, updated = 0, 0
    for record in incoming:
        _, was_created = store.upsert_by_email(record)
        created += int(was_created)
        updated += int(not was_created)
    return {"created": created, "updated": updated, "total_processed": len(incoming)}
