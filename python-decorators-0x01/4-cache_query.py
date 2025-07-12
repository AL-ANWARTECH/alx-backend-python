from datetime import datetime
import time
import sqlite3
import functools

# Global cache for queries
query_cache = {}

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

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract 'query' from either args or kwargs
        if 'query' in kwargs:
            query = kwargs['query']
        elif len(args) > 0:
            query = args[0]
        else:
            raise ValueError("Query argument not provided.")

        if query in query_cache:
            print("Using cached result for query.")
            return query_cache[query]
        print("Executing query and caching result.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
