"""
services/file_writer.py

Handles writing JSON data back to disk. Used for both the processed
output file and the updated customer database.

Single Responsibility: this class only knows how to write JSON files.
It mirrors FileReader so reading and writing stay symmetric.
"""

import json
import os


class FileWriter:
    """Writes Python objects to disk as formatted JSON files."""

    @staticmethod
    def write_json(file_path: str, data) -> None:
        """Write data to file_path as pretty-printed JSON, creating folders as needed."""
        folder = os.path.dirname(file_path)
        if folder:
            os.makedirs(folder, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
