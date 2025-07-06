# Python Generators - Stream SQL Rows

## Objective

Create a Python generator that streams rows from a MySQL database table `user_data` one by one.

## Project Setup

1. Install MySQL and create a user with proper privileges.
2. Place your `user_data.csv` in the `python-generators-0x00` directory.
3. Update MySQL credentials in `seed.py`.

## Structure

- `connect_db()` – Connects to MySQL server.
- `create_database(connection)` – Creates `ALX_prodev` DB if it doesn't exist.
- `connect_to_prodev()` – Connects to `ALX_prodev` DB.
- `create_table(connection)` – Creates `user_data` table.
- `insert_data(connection, csv_file)` – Loads CSV data into the table.
- `stream_users(connection)` – Generator that yields rows one-by-one.

## Sample Usage

```bash
$ ./0-main.py
connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'name1', 'email1', 23), ...]
