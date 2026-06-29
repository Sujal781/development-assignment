# Employee Records API

A FastAPI service that stores employee records in an Excel file
instead of a traditional database, with full CRUD plus two
integration endpoints for talking to external APIs.

This is a sibling project to `customer_demo/` - same design philosophy
(single responsibility, one class per job, no business logic in the
HTTP layer), just a different domain.

## Project Structure

```
employee_api/
│
├── app/
│   ├── main.py             # FastAPI app - routes only, no business logic
│   ├── config.py           # file path + external API URLs (env-overridable)
│   ├── models.py           # Pydantic request/response schemas
│   ├── excel_store.py      # all Excel read/write logic (CRUD)
│   └── external_client.py  # send-to / fetch-from external APIs
│
├── data/
│   └── employees.xlsx      # the "database" - seeded with 3 sample employees
│
├── tests/
│   └── test_excel_store.py # unit tests for the storage layer (stdlib only)
│
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

```bash
cd employee_api
pip install -r requirements.txt
```

## Running the API

```bash
uvicorn app.main:app --reload
```

Then open **http://127.0.0.1:8000/docs** for interactive Swagger docs
where you can try every endpoint directly in the browser.

## Running the Tests

The storage layer's tests only need `openpyxl` (not the full
`requirements.txt`), so you can sanity-check that logic even before
installing FastAPI:

```bash
python -m unittest tests/test_excel_store.py -v
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/employees` | List all employees |
| GET | `/employees/{employee_id}` | Get one employee |
| POST | `/employees` | Create a new employee |
| PUT | `/employees/{employee_id}` | Update one or more fields |
| DELETE | `/employees/{employee_id}` | Delete an employee |
| POST | `/employees/{employee_id}/send` | Push one employee to an external API |
| POST | `/employees/sync-external` | Pull records from an external API and import them |

### Example requests

```bash
# List everyone
curl http://127.0.0.1:8000/employees

# Create a new employee
curl -X POST http://127.0.0.1:8000/employees \
  -H "Content-Type: application/json" \
  -d '{"name":"Dana White","email":"dana@company.com","department":"Marketing","designation":"Lead","salary":85000}'

# Update just the salary
curl -X PUT http://127.0.0.1:8000/employees/EMP1001 \
  -H "Content-Type: application/json" \
  -d '{"salary":98000}'

# Delete an employee
curl -X DELETE http://127.0.0.1:8000/employees/EMP1003

# Push EMP1001's record out to the external "send" API
curl -X POST http://127.0.0.1:8000/employees/EMP1001/send

# Pull records in from the external "fetch" API and import them
curl -X POST http://127.0.0.1:8000/employees/sync-external
```

## About the External API URLs

The task description says to "send employee data to another API
endpoint" and "consume data from an external API" without naming real
ones, so this demo points at two free public test services by
default (see `app/config.py`):

- **Sending** defaults to `https://httpbin.org/post`, which just
  echoes back whatever JSON you send it - so you can confirm the
  outbound call actually fires and see exactly what was sent.
- **Fetching** defaults to `https://jsonplaceholder.typicode.com/users`,
  a free fake-data API that returns a list of user-like records - so
  you can confirm the inbound sync actually works end-to-end.

Override either one with real URLs via environment variables (see
`.env.example`) once you have actual endpoints to integrate with. If
the real "fetch" API returns a different shape than
`jsonplaceholder`'s `/users` response, adjust the field mapping in
`app/external_client.py`'s `fetch_external_employees()` to match.

## Design Notes

- **`employee_id` generation** mirrors the GCID logic from the customer
  demo - sequential IDs like `EMP1001`, `EMP1002`, scanning existing
  records for the highest number in use.
- **`/employees/sync-external` reuses the same idea as the customer
  demo's identity resolution**: incoming records are matched by email.
  If a match exists, the record is updated in place (reusing its
  `employee_id`); if not, a new record is created. See
  `ExcelEmployeeStore.upsert_by_email()`.
- **Known limitation**: using a flat Excel file as a database means
  every read/write reloads and re-saves the whole workbook, and the
  in-process lock only protects against concurrent requests within a
  single running server - it won't help if you ever run multiple
  worker processes. That's an intentional simplification for a demo;
  swapping `ExcelEmployeeStore` for a real database later wouldn't
  require any changes to `app/main.py` or `app/external_client.py`.

## What Was and Wasn't Tested Here

This project was generated in an environment without internet access,
so `fastapi`, `uvicorn`, `httpx`, and `pydantic` couldn't be installed
or run here. What *was* tested directly, with all tests passing:

- `ExcelEmployeeStore` (create, read, update, delete, upsert-by-email)
  via `tests/test_excel_store.py`, since it only depends on `openpyxl`,
  which was available.

The FastAPI routes and external API client follow standard, well-worn
patterns for these libraries, but you should run
`uvicorn app.main:app --reload` and try the endpoints (or run `pytest`
against the routes, if you add route-level tests) on your own machine
to confirm the HTTP layer end-to-end.
