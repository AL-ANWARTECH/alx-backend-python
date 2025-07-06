import mysql.connector

# Generator that fetches users in batches from the database
def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='AlAnwarTech',
            password='AnwarSagir@360',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM user_data")
        total_rows = cursor.fetchone()['total']
        offset = 0

        while offset < total_rows:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s",
                (batch_size, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batch_size

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        
# Function that processes each batch to filter users over age 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)