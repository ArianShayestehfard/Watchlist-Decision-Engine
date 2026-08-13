import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_NAME = os.path.join(BASE_DIR, "database", "watchlist.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

