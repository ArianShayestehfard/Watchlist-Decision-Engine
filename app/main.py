from database import get_connection

connection = get_connection()

print("Database connection successful!")

connection.close()