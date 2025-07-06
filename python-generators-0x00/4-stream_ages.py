import mysql.connector

# Generator that yields user age one by one
def stream_user_ages():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='AlAnwarTech',
            password='AnwarSagir@360',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield age

        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        
# Function to compute avaerage age using the generator
def compute_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():
        total_age += age
        count += 1

    if count > 0:
        average = total_age / count
        print(f"Average age: {average:.2f}")
    else:
        print("No users found to compute average age.")