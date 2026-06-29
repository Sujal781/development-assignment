"""
tests/test_excel_store.py

Unit tests for ExcelEmployeeStore. Deliberately uses only the standard
library's `unittest` (no pytest, no FastAPI, no pydantic) so this test
suite can run even before you've installed the rest of requirements.txt
- it only needs openpyxl, the same as excel_store.py itself.

Run with (from the employee_api/ folder):
    python -m unittest tests/test_excel_store.py -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.excel_store import ExcelEmployeeStore

TEST_FILE = "test_employees_unittest.xlsx"


class TestExcelEmployeeStore(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
        self.store = ExcelEmployeeStore(TEST_FILE)

    def tearDown(self):
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)

    def _sample(self, **overrides):
        data = {
            "name": "Alice",
            "email": "alice@co.com",
            "department": "Eng",
            "designation": "Engineer",
            "salary": 90000,
        }
        data.update(overrides)
        return data

    def test_starts_empty(self):
        self.assertEqual(self.store.get_all(), [])

    def test_create_assigns_sequential_ids(self):
        e1 = self.store.create(self._sample())
        e2 = self.store.create(self._sample(name="Bob", email="bob@co.com"))
        self.assertEqual(e1["employee_id"], "EMP1001")
        self.assertEqual(e2["employee_id"], "EMP1002")

    def test_get_by_id_found_and_missing(self):
        created = self.store.create(self._sample())
        self.assertEqual(self.store.get_by_id(created["employee_id"])["name"], "Alice")
        self.assertIsNone(self.store.get_by_id("EMP9999"))

    def test_update_changes_only_given_fields(self):
        created = self.store.create(self._sample())
        updated = self.store.update(created["employee_id"], {"salary": 100000})
        self.assertEqual(updated["salary"], 100000)
        self.assertEqual(updated["department"], "Eng")  # unchanged

    def test_update_missing_id_returns_none(self):
        self.assertIsNone(self.store.update("EMP9999", {"salary": 1}))

    def test_delete_removes_record(self):
        created = self.store.create(self._sample())
        self.assertTrue(self.store.delete(created["employee_id"]))
        self.assertIsNone(self.store.get_by_id(created["employee_id"]))

    def test_delete_missing_id_returns_false(self):
        self.assertFalse(self.store.delete("EMP9999"))

    def test_upsert_by_email_updates_existing(self):
        created = self.store.create(self._sample())
        record, was_created = self.store.upsert_by_email(
            self._sample(name="Alice Updated")
        )
        self.assertFalse(was_created)
        self.assertEqual(record["employee_id"], created["employee_id"])
        self.assertEqual(record["name"], "Alice Updated")

    def test_upsert_by_email_creates_new(self):
        record, was_created = self.store.upsert_by_email(
            self._sample(name="New Person", email="new@co.com")
        )
        self.assertTrue(was_created)
        self.assertEqual(record["employee_id"], "EMP1001")


if __name__ == "__main__":
    unittest.main()
