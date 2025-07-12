import sqlite3


class DatabaseConnection:
    def __init__(self, db_file):
        """Initialize the database connection."""
        self.db_file = db_file
        self.connection = None

    def __enter__(self):
        """Open the database connection and return the connection object."""
        self.connection = sqlite3.connect(self.db_file)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        """"Close the database connection. Handle exceptions if needed."""
        if self.connection:
            self.connection.close()
        

if __name__ == "__main__":
    # Example usage
    db_file = "example.db"
    
    with DatabaseConnection(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
        