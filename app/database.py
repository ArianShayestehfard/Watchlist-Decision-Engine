import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_NAME = os.path.join(BASE_DIR, "database", "watchlist.db")


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection

def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS movies (
                                                         id INTEGER PRIMARY KEY,
                                                         tmdb_id INTEGER UNIQUE,
                                                         title TEXT NOT NULL,
                                                         release_date TEXT,
                                                         runtime INTEGER,
                                                         rating REAL,
                                                         overview TEXT
                   )
                   """)


    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS genres (
                                                         id INTEGER PRIMARY KEY,
                                                         tmdb_id INTEGER UNIQUE,
                                                         name TEXT NOT NULL
                   )
                   """)


    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS movie_genres (
                                                               movie_id INTEGER,
                                                               genre_id INTEGER,

                                                               FOREIGN KEY(movie_id) REFERENCES movies(id),
                                                               FOREIGN KEY(genre_id) REFERENCES genres(id)
                       )
                   """)


    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ratings (
                                                          id INTEGER PRIMARY KEY,
                                                          movie_id INTEGER,
                                                          user_rating REAL,

                                                          FOREIGN KEY(movie_id) REFERENCES movies(id)
                       )
                   """)


    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS watchlist (
                                                            id INTEGER PRIMARY KEY,
                                                            movie_id INTEGER UNIQUE,
                                                            status TEXT DEFAULT 'planned',

                                                            FOREIGN KEY(movie_id) REFERENCES movies(id)
                       )
                   """)


    connection.commit()
    connection.close()

    print("Tables created successfully!")
