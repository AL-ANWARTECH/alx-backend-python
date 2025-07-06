import mysql.connector

# Function that fetches one page of users from the DB
def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="AlAnwarTech",
            password="AnwarSagir@360", 
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []

# Generator that lazily paginates using the above function
def lazypaginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
