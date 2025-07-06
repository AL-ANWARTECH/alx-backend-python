import mysql.connector
import csv
import uuid

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='AnwarSagir@360',

        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
def connect_to_prodev_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='AnwarSagir@360',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name varchar(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: creating table: {err}")

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']
                
                cursor.execute("""
                    select * from user_data where email = %s
                """, (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error: inserting data: {e}")

def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    row = cursor.fetchone()
    while row :
        yield row
        row = cursor.fetchone()
    cursor.close()