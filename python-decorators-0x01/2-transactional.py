from datetime import datetime
import sqlite3
import functools

# Decorator to manage database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            conn.commit()
            return result
        except Exception :
            conn.rollback()
            raise
    return wrapper

@with_db_connection
@transactional
def update_user(conn, user_id, name, email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
    return cursor.rowcount
# Update user with automatic transaction management
user_id = 1