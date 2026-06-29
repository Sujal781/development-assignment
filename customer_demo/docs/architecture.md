# Architecture

This demo is a minimal, single-machine version of an enterprise batch
identity-resolution pipeline. It demonstrates the same core idea
(match an incoming record to an existing identity, or mint a new one)
without any of the infrastructure (queues, databases, cloud storage)
that a production MDM platform would use.

## Component Diagram

```
                  app.py
                     │
                     ▼
              services/FileReader
                     │
                     ▼
            services/IdentityService
              │               │
              ▼               ▼
   database/customers_db   services/GCIDGenerator
              │               │
              └───────┬───────┘
                      ▼
              services/FileWriter
                      │
                      ▼
        output/processed_customers.json
```

## Design Principles Demonstrated

- **Single Responsibility Principle** - each class does exactly one job:
  `FileReader` only reads, `FileWriter` only writes, `GCIDGenerator` only
  generates IDs, and `IdentityService` only makes the match/no-match decision.
- **Modularity** - reading, identity lookup, ID generation, and writing are
  four separate, independently testable pieces.
- **Loose Coupling** - `app.py` orchestrates the workflow but contains no
  business logic itself; it just calls the services in order.
- **Extensibility** - the JSON file database can be swapped for a real
  database (Postgres, DynamoDB, etc.) and the local input/output folders
  can be swapped for S3 buckets, with no changes needed to
  `IdentityService` or `GCIDGenerator`.
