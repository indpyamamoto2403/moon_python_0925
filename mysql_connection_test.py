import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host="moon-dba",
            user="indp",
            password="secret",
            database="moon"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    test_mysql_connection()