## Getting Started with Python Generators (ALX Backend)

This repository provides a seeding script (`seed.py`) to set up a MySQL database and a generator function to stream rows from the `user_data` table one by one.

### Prerequisites

* Python 3.x
* MySQL Server running locally
* Python package: `mysql-connector-python`

  ```bash
  pip install mysql-connector-python
  ```

### Project Structure

```
alx-backend-python/
└── python-generators-0x00/
    ├── seed.py         # Seeding and generator logic
    ├── user_data.csv   # Sample data to populate the table
    └── 0-main.py       # Example usage script
```

### Usage

1. **Seed the Database**

   ```bash
   ./0-main.py
   ```

   This will:

   * Connect to MySQL server (`connect_db`)
   * Create the `ALX_prodev` database if it doesn’t exist (`create_database`)
   * Connect to `ALX_prodev` (`connect_to_prodev`)
   * Create the `user_data` table (`create_table`)
   * Populate the table from `user_data.csv` (`insert_data`)
   * Print the first 5 rows to verify

2. **Stream Rows via Generator**

   ```python
   from seed import connect_to_prodev, stream_user_data

   conn = connect_to_prodev()
   for row in stream_user_data(conn):
       print(row)
   ```

   * `stream_user_data` yields one record at a time from the `user_data` table.

### Functions Overview

* `connect_db()`: Connects to MySQL server (no DB).
* `create_database(connection)`: Creates `ALX_prodev` database if missing.
* `connect_to_prodev()`: Connects to `ALX_prodev`.
* `create_table(connection)`: Creates `user_data` table.
* `insert_data(connection, data_file)`: Inserts CSV data into the table.
* `stream_user_data(connection)`: **Generator** yielding rows one by one.

---

*Ensure your MySQL credentials in `seed.py` match your local setup.*
