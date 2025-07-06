import mysql.connector

# Generator to stream users in batches
def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="AlAnwarTech",  
            password="AnwarSagir@360",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        offset = 0

        while True:
            cursor.execute(
                "SELECT * FROM user_data LIMIT %s OFFSET %s", (batch_size, offset)
            )
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows
            offset += batch_size


        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        

# Generator that yields users over age 25
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user["age"] > 25:
                return user