print("HELLO WORLD")

import mysql.connector

def fetch_m_prompt_values():
    connection = mysql.connector.connect(
        host="moon-db",
        user="indp",
        password="secret",
        database="moon"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM m_prompt")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

m_prompt_values = fetch_m_prompt_values()
for value in m_prompt_values:
     print(value)