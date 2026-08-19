import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_DIR = os.path.join(BASE_DIR, "database")
DATABASE_NAME = os.path.join(DATABASE_DIR, "watchlist.db")


def get_connection():
    os.makedirs(DATABASE_DIR, exist_ok=True)

    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS movies (
                                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         imdb_id TEXT UNIQUE,
                                                         title TEXT NOT NULL,
                                                         release_date TEXT,
                                                         runtime INTEGER,
                                                         rating REAL,
                                                         overview TEXT
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS genres (
                                                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                         name TEXT NOT NULL UNIQUE
                   )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS movie_genres (
                                                               movie_id INTEGER,
                                                               genre_id INTEGER,

                                                               PRIMARY KEY (movie_id, genre_id),

                       FOREIGN KEY (movie_id)
                       REFERENCES movies(id)
                       ON DELETE CASCADE,

                       FOREIGN KEY (genre_id)
                       REFERENCES genres(id)
                       ON DELETE CASCADE
                       )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ratings (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          movie_id INTEGER,
                                                          user_rating REAL,

                                                          FOREIGN KEY (movie_id)
                       REFERENCES movies(id)
                       ON DELETE CASCADE
                       )
                   """)

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS watchlist (
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            movie_id INTEGER UNIQUE,
                                                            status TEXT DEFAULT 'planned',

                                                            FOREIGN KEY (movie_id)
                       REFERENCES movies(id)
                       ON DELETE CASCADE
                       )
                   """)

    connection.commit()
    connection.close()

    print("Tables created successfully!")