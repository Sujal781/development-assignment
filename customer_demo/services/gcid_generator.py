"""
services/gcid_generator.py

Responsible for generating new Global Customer IDs (GCIDs).
A GCID looks like "GC1001", "GC1002", and so on.

Single Responsibility: this class only knows how to produce the
*next* available GCID. It does not know about emails, files, or
the database structure beyond the "gcid" field it needs to scan.
"""


class GCIDGenerator:
    """Generates the next available GCID based on existing records."""

    PREFIX = "GC"
    STARTING_NUMBER = 1000  # so the first ever generated GCID is GC1001

    def __init__(self, existing_database: list):
        """
        existing_database: list of dicts, each containing a "gcid" key,
        e.g. [{"gcid": "GC1001", "email": "alice@gmail.com"}, ...]
        """
        self._next_number = self._compute_next_number(existing_database)

    def _compute_next_number(self, existing_database: list) -> int:
        """Find the highest existing GCID number in the database and return the next one."""
        highest = self.STARTING_NUMBER
        for record in existing_database:
            gcid = record.get("gcid", "")
            if gcid.startswith(self.PREFIX):
                try:
                    number = int(gcid[len(self.PREFIX):])
                    highest = max(highest, number)
                except ValueError:
                    continue
        return highest + 1

    def generate(self) -> str:
        """Generate the next GCID and advance the internal counter."""
        new_gcid = f"{self.PREFIX}{self._next_number}"
        self._next_number += 1
        return new_gcid
