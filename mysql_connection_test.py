import mysql.connector
from mysql.connector import Error

def test_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host='your_host',
            database='your_database',
            user='your_username',
            password='your_password'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

def fetch_m_prompt_values():
    try:
        connection = mysql.connector.connect(
            host="moon-db",
            user="indp",
            password="secret",
            database="moon"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM m_prompt")
        results = cursor.fetchall()
        return results
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    print("HELLO WORLD")
    m_prompt_values = fetch_m_prompt_values()
    for value in m_prompt_values:
        print(value)
    test_mysql_connection()