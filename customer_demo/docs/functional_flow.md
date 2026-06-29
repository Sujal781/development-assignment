# Functional Flow

This describes the demo from a business/functional point of view -
no code, just the decision process for each incoming customer.

```
            Input Folder
       (customer_input.json)
                 │
                 ▼
       Read Customer Record
                 │
                 ▼
     Search Customer Database
                 │
        ┌────────┴────────┐
        │                 │
      Found            Not Found
        │                 │
  Use Existing GCID   Generate New GCID
        │                 │
        └────────┬────────┘
                 ▼
       Create Updated Record
                 │
                 ▼
            Output Folder
     (processed_customers.json)
```

## Worked Example

**Existing database:**

```json
[
  { "gcid": "GC1001", "email": "alice@gmail.com" },
  { "gcid": "GC1002", "email": "bob@gmail.com" }
]
```

**Incoming batch:**

```json
[
  { "name": "Alice", "email": "alice@gmail.com" },
  { "name": "John", "email": "john@gmail.com" }
]
```

**Processing:**

- Alice -> found in database -> reuse `GC1001`
- John -> not found -> generate `GC1003` -> add to database

**Output:**

```json
[
  { "name": "Alice", "email": "alice@gmail.com", "gcid": "GC1001" },
  { "name": "John", "email": "john@gmail.com", "gcid": "GC1003" }
]
```

**Database after the run:**

```json
[
  { "gcid": "GC1001", "email": "alice@gmail.com" },
  { "gcid": "GC1002", "email": "bob@gmail.com" },
  { "gcid": "GC1003", "email": "john@gmail.com" }
]
```
