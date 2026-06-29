"""
app/models.py

Pydantic schemas defining the shape of employee data as it crosses
the API boundary. These are request/response models only - the
Excel storage layer (excel_store.py) works with plain dicts and
never imports anything from here, so the storage logic stays
independent of how the data is validated or presented over HTTP.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    designation: str
    salary: float


class EmployeeCreate(EmployeeBase):
    """Fields required to create a new employee. No employee_id here -
    the server generates that, the same way GCIDs are generated in the
    customer demo."""
    pass


class EmployeeUpdate(BaseModel):
    """Every field is optional, so a single PUT request can update just
    one field (e.g. only `salary`) without resending the whole record."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = None


class Employee(EmployeeBase):
    """Full employee record, as returned by the API."""
    employee_id: str
