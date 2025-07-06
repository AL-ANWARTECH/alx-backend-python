import mysql.connector

def stream_users():
    try:

        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='AlAnwarTech',
            password='AnwarSagir@360',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # Fetch rows one by one
        for row in cursor:
            yield row

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return

        