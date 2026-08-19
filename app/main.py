from database import get_connection

connection = get_connection()
cursor = connection.cursor()
cursor.execute("SELECT id, title, status FROM movies")
for row in cursor.fetchall():
    print(row)
connection.close()