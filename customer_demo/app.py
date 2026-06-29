"""
app.py

Entry point for the Customer Identity Resolution demo.

Flow:
    1. Read incoming customers from input/customer_input.json
    2. Load the existing customer database from database/customers_db.json
    3. For each incoming customer, resolve their identity:
         - existing email -> reuse the existing GCID
         - new email      -> generate a new GCID and register it
    4. Write the enriched customer records to output/processed_customers.json
    5. Persist the (possibly updated) database back to database/customers_db.json

This file only orchestrates the workflow - it contains no business
logic itself. That keeps it loosely coupled to the services it uses.

Run with:
    python app.py
"""

from services.file_reader import FileReader
from services.file_writer import FileWriter
from services.identity_service import IdentityService
from models.customer import Customer

INPUT_FILE = "input/customer_input.json"
DATABASE_FILE = "database/customers_db.json"
OUTPUT_FILE = "output/processed_customers.json"


def main():
    print("Starting Customer Identity Resolution demo...\n")

    # Step 1: Read the incoming customer batch
    raw_customers = FileReader.read_json(INPUT_FILE)
    print(f"Loaded {len(raw_customers)} customer(s) from {INPUT_FILE}")

    # Step 2: Load the existing customer database
    database = FileReader.read_json(DATABASE_FILE)
    print(f"Loaded {len(database)} existing record(s) from {DATABASE_FILE}\n")

    # Step 3: Resolve identities one customer at a time
    identity_service = IdentityService(database)
    processed_customers = []

    for raw in raw_customers:
        customer = Customer.from_dict(raw)

        was_new = identity_service.is_new_customer(customer.email)
        customer.gcid = identity_service.resolve(customer.email)
        processed_customers.append(customer)

        label = "NEW" if was_new else "EXISTING"
        print(f"  {customer.name:<10} {customer.email:<25} -> {customer.gcid}  [{label}]")

    # Step 4: Write the enriched output file
    output_data = [c.to_dict() for c in processed_customers]
    FileWriter.write_json(OUTPUT_FILE, output_data)
    print(f"\nWrote {len(output_data)} processed record(s) to {OUTPUT_FILE}")

    # Step 5: Persist the updated database (includes any newly generated GCIDs)
    FileWriter.write_json(DATABASE_FILE, identity_service.database)
    print(f"Updated database now has {len(identity_service.database)} record(s) in {DATABASE_FILE}")

    print("\nDone.")


if __name__ == "__main__":
    main()
