"""
services/file_reader.py

Handles reading JSON data from disk. Used both for the incoming
customer input file and the existing customer database.

Single Responsibility: this class only knows how to read JSON files.
It has no idea what a "customer" or a "GCID" is.
"""

import json
import os


class FileReader:
    """Reads JSON files from the filesystem and returns plain Python objects."""

    @staticmethod
    def read_json(file_path: str) -> list:
        """
        Read a JSON file and return its contents as a list of dicts.

        Returns an empty list if the file does not exist or is empty,
        so callers never need to special-case a "first run" scenario.
        """
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
