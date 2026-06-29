# Technical Flow

This describes the same process from a code/class point of view -
which class calls which, and what data passes between them.

```
                     app.py
                        │
                        ▼
              FileReader.read_json()
              (input/customer_input.json)
              (database/customers_db.json)
                        │
                        ▼
            IdentityService(database)
                        │
              ┌─────────┴─────────┐
              │                   │
   IdentityService._email_index   GCIDGenerator
   (dict lookup by email)         (.generate())
              │                   │
              └─────────┬─────────┘
                        ▼
              IdentityService.resolve(email)
                  returns a GCID string
                        │
                        ▼
              Customer.gcid = gcid
                        │
                        ▼
              FileWriter.write_json()
       (output/processed_customers.json)
       (database/customers_db.json, updated)
```

## Class Responsibilities

| Class | File | Responsibility |
|---|---|---|
| `Customer` | `models/customer.py` | Plain data model for a customer record |
| `FileReader` | `services/file_reader.py` | Reads any JSON file into a list of dicts |
| `IdentityService` | `services/identity_service.py` | Decides reuse-vs-generate for each email |
| `GCIDGenerator` | `services/gcid_generator.py` | Produces the next sequential GCID |
| `FileWriter` | `services/file_writer.py` | Writes any data structure to a JSON file |
| `app.py` | `app.py` | Orchestrates the five-step workflow end to end |

## Sequence Per Customer

1. `app.py` builds a `Customer` from the raw input dict.
2. `app.py` asks `IdentityService.resolve(customer.email)`.
3. `IdentityService` checks its internal `_email_index` (built from the
   database) for that email.
4. If found, the existing GCID is returned immediately.
5. If not found, `IdentityService` asks `GCIDGenerator.generate()` for a
   new GCID, registers the email + GCID in its in-memory database, and
   returns the new GCID.
6. `app.py` assigns the returned GCID to `customer.gcid` and moves to the
   next customer.

After all customers are processed, `app.py` writes the enriched list to
the output file and writes `identity_service.database` (now containing
any newly added customers) back to the database file.
