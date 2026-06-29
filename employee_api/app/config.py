"""
app/config.py

Centralizes configuration so file paths and external API URLs are
never hardcoded inside the business logic. Every value here can be
overridden with an environment variable (e.g. via a .env file) so
you can point this at different endpoints without touching code.

NOTE ON THE DEFAULT EXTERNAL URLS:
The assignment says "send employee data to another API endpoint" and
"consume data from an external API" without naming real ones, so this
demo wires up to two public test services as sensible stand-ins:

  - EXTERNAL_SEND_API_URL defaults to https://httpbin.org/post,
    which simply echoes back whatever JSON you POST to it - useful
    for confirming the outbound call actually works.
  - EXTERNAL_FETCH_API_URL defaults to https://jsonplaceholder.typicode.com/users,
    a free fake-data API that returns a list of user-like records -
    useful for confirming the inbound/sync call actually works.

Swap either one for a real internal API URL whenever you have one.
"""

import os

# Path to the Excel file that acts as the employee "database"
EXCEL_FILE_PATH = os.getenv("EMPLOYEE_EXCEL_PATH", "data/employees.xlsx")

# Where this API sends an employee record when asked to push one out
EXTERNAL_SEND_API_URL = os.getenv(
    "EXTERNAL_SEND_API_URL", "https://httpbin.org/post"
)

# Where this API pulls records from when asked to sync/import
EXTERNAL_FETCH_API_URL = os.getenv(
    "EXTERNAL_FETCH_API_URL", "https://jsonplaceholder.typicode.com/users"
)
