"""
models/customer.py

Defines the Customer data model used throughout the application.

A Customer represents a single customer record, either incoming
(freshly read from the input file, with no GCID yet) or resolved
(after the IdentityService has assigned it a GCID).
"""


class Customer:
    """Represents a single customer record."""

    def __init__(self, name: str, email: str, gcid: str = None):
        self.name = name
        self.email = email
        self.gcid = gcid

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        """Build a Customer instance from a plain dictionary (e.g. parsed JSON)."""
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            gcid=data.get("gcid"),
        )

    def to_dict(self) -> dict:
        """Convert the Customer instance back into a plain dictionary for JSON output."""
        return {
            "name": self.name,
            "email": self.email,
            "gcid": self.gcid,
        }

    def __repr__(self) -> str:
        return f"Customer(name={self.name!r}, email={self.email!r}, gcid={self.gcid!r})"
