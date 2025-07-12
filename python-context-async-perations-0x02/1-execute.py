import sqlite3


class ExecuteQuery:
    def __init__(self, db_file, query, params=None):
        """Intialize with database name, query and optional parameters."""
        self.db_file =db_file
        self.query = query
        self.params = params or []
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """ Establish DB connection, execute the query and return results."""
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        """"Close cursor and connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    db_file = "example.db"
    query = "SELECT * FROM users WHERE age > ?"
    params = [25]

    with ExecuteQuery(db_file, query, params) as results:
        for row in results:
            print(row)

