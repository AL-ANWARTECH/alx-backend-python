from datetime import datetime
import time
import sqlite3
import functools

# Decorator to manage database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(conn, *args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(conn, *args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
            print("All attempts failed.")
            raise last_exception
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Fetch users with retry mechanism
users = fetch_users_with_retry()
print(users)