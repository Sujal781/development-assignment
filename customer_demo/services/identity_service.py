"""
services/identity_service.py

Implements the identity resolution logic: given a customer's email,
decide whether they already exist in the database (reuse their GCID)
or are new (generate and register a fresh GCID).

This is the heart of the demo - everything else (file reading,
writing, GCID generation) just supports this one decision.
"""

from services.gcid_generator import GCIDGenerator


class IdentityService:
    """Resolves customer identities against the existing customer database."""

    def __init__(self, database: list):
        """
        database: the in-memory list of existing customer records,
        each shaped like {"gcid": "GC1001", "email": "alice@gmail.com"}.
        This list is mutated in place as new customers are resolved,
        so callers can persist it back to disk afterwards.
        """
        self.database = database
        self._email_index = {record["email"]: record["gcid"] for record in database}
        self.gcid_generator = GCIDGenerator(database)

    def resolve(self, email: str) -> str:
        """
        Return the GCID for the given email.

        - If the email already exists in the database, return its existing GCID.
        - Otherwise, generate a brand new GCID, register the customer in the
          database, and return the new GCID.
        """
        existing_gcid = self._email_index.get(email)
        if existing_gcid:
            return existing_gcid

        new_gcid = self.gcid_generator.generate()
        self._register(email, new_gcid)
        return new_gcid

    def is_new_customer(self, email: str) -> bool:
        """Convenience check: was this email already known before resolve() was called?"""
        return email not in self._email_index

    def _register(self, email: str, gcid: str) -> None:
        """Add a newly resolved customer to the in-memory database."""
        record = {"gcid": gcid, "email": email}
        self.database.append(record)
        self._email_index[email] = gcid
