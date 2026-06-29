# Customer Identity Resolution Demo

A minimal, runnable demo of a batch customer identity-resolution
pipeline: it ingests a batch of customers, matches them against an
existing customer database by email, reuses the GCID (Global Customer
ID) when a match is found, and generates a new GCID when it isn't.

This is intentionally small (~150-200 lines across all files) so it's
easy to read and demo end-to-end, while still mirroring the shape of a
real enterprise MDM / identity-resolution flow.

## Project Structure

```
customer_demo/
│
├── app.py                          # entry point - orchestrates the workflow
│
├── input/
│   └── customer_input.json         # incoming batch of customers to process
│
├── database/
│   └── customers_db.json           # existing customers + their GCIDs
│
├── output/
│   └── processed_customers.json    # generated automatically when you run app.py
│
├── services/
│   ├── file_reader.py              # reads JSON files
│   ├── identity_service.py         # match-or-generate decision logic
│   ├── gcid_generator.py           # produces new sequential GCIDs
│   └── file_writer.py              # writes JSON files
│
├── models/
│   └── customer.py                 # Customer data model
│
├── docs/
│   ├── architecture.md             # component diagram + design principles
│   ├── functional_flow.md          # business-level flow + worked example
│   └── technical_flow.md           # class-level flow + sequence of calls
│
└── README.md
```

## How to Run

From inside the `customer_demo/` folder:

```bash
python app.py
```

You should see output like:

```
Starting Customer Identity Resolution demo...

Loaded 2 customer(s) from input/customer_input.json
Loaded 2 existing record(s) from database/customers_db.json

  Alice      alice@gmail.com           -> GC1001  [EXISTING]
  John       john@gmail.com            -> GC1003  [NEW]

Wrote 2 processed record(s) to output/processed_customers.json
Updated database now has 3 record(s) in database/customers_db.json

Done.
```

Run it again and John will now show as `[EXISTING]`, since he was added
to `database/customers_db.json` on the first run.

## Try It Yourself

Add more customers to `input/customer_input.json` (mix of known and
unknown emails) and re-run `python app.py` to see new GCIDs minted only
for the genuinely new emails.

## Design Principles

- **Single Responsibility** - each class does exactly one thing.
- **Modularity** - reading, identity lookup, ID generation, and writing
  are four separate, independently testable services.
- **Loose Coupling** - `app.py` orchestrates without containing any
  business logic itself.
- **Extensibility** - swap the JSON file "database" for a real database,
  or swap the local folders for S3 buckets, without touching
  `IdentityService` or `GCIDGenerator`.

See `docs/architecture.md`, `docs/functional_flow.md`, and
`docs/technical_flow.md` for more detail and diagrams.
