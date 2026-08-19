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
                       FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE,
                       FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
                       )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS ratings (
                                                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                          movie_id INTEGER,
                                                          user_rating REAL,
                                                          FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
                       )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS watchlist (
                                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            movie_id INTEGER UNIQUE,
                                                            status TEXT DEFAULT 'want_to_watch',
                                                            FOREIGN KEY (movie_id) REFERENCES movies(id) ON DELETE CASCADE
                       )
                   """)
    connection.commit()
    connection.close()
    print("Tables created successfully!")

def add_movie(imdb_id, title, release_date, runtime, rating, overview):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   INSERT OR IGNORE INTO movies (imdb_id, title, release_date, runtime, rating, overview)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, (imdb_id, title, release_date, runtime, rating, overview))
    connection.commit()
    connection.close()
    print("Movie added successfully!")

def get_movies():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, imdb_id, title, release_date, runtime, rating FROM movies")
    movies = cursor.fetchall()
    connection.close()
    return movies

def update_movie_rating(movie_id, new_rating):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE movies SET rating = ? WHERE id = ?", (new_rating, movie_id))
    connection.commit()
    connection.close()
    print("Movie rating updated successfully!")

def delete_movie(movie_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
    connection.commit()
    connection.close()
    print("Movie deleted successfully!")

def get_movie_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, imdb_id, title, release_date, runtime, rating FROM movies WHERE title = ?", (title,))
    movie = cursor.fetchone()
    connection.close()
    return movie

def add_movies_batch(titles):
    from omdb_api import search_movie
    added = []
    failed = []
    for title in titles:
        movie_data = search_movie(title)
        if not movie_data:
            failed.append(title)
            continue
        add_movie(movie_data["imdb_id"], movie_data["title"], movie_data["release_date"], movie_data["runtime"], movie_data["rating"], movie_data["overview"])
        added.append(movie_data["title"])
    return {"added": added, "failed": failed}

def update_movie_status(movie_id, new_status):
    valid_statuses = ("want_to_watch", "watching", "watched")
    if new_status not in valid_statuses:
        print(f"Error: invalid status '{new_status}'. Must be one of {valid_statuses}.")
        return
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM watchlist WHERE movie_id = ?", (movie_id,))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE watchlist SET status = ? WHERE movie_id = ?", (new_status, movie_id))
    else:
        cursor.execute("INSERT INTO watchlist (movie_id, status) VALUES (?, ?)", (movie_id, new_status))
    connection.commit()
    connection.close()
    print("Movie status updated successfully!")

def get_movies_by_status(status):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT movies.id, movies.imdb_id, movies.title, movies.release_date, movies.runtime, movies.rating, watchlist.status
                   FROM movies JOIN watchlist ON movies.id = watchlist.movie_id
                   WHERE watchlist.status = ?
                   """, (status,))
    movies = cursor.fetchall()
    connection.close()
    return movies

def get_movie_by_id(movie_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title FROM movies WHERE id = ?", (movie_id,))
    movie = cursor.fetchone()
    connection.close()
    return movie

def get_movie_by_imdb_id(imdb_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title FROM movies WHERE imdb_id = ?", (imdb_id,))
    movie = cursor.fetchone()
    connection.close()
    return movie

def find_movies_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, imdb_id FROM movies WHERE LOWER(title) LIKE ?", (f"%{title.lower()}%",))
    movies = cursor.fetchall()
    connection.close()
    return movies

def get_movie_by_exact_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, imdb_id FROM movies WHERE LOWER(title) = ?", (title.lower(),))
    movie = cursor.fetchone()
    connection.close()
    return movie

def find_movies_by_title(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, imdb_id FROM movies WHERE LOWER(title) LIKE ?", (f"%{title.lower()}%",))
    movies = cursor.fetchall()
    connection.close()
    return movies
from movie_list import POPULAR_MOVIES
import time

def import_500_movies(delay=0.5):
    added = 0
    failed = 0

    for i, title in enumerate(POPULAR_MOVIES, 1):
        print(f"[{i}/{len(POPULAR_MOVIES)}] Processing: {title}")
        data = search_movie(title)

        if data:
            add_movie(
                imdb_id=data.get("imdb_id"),
                title=data.get("title"),
                release_date=data.get("release_date"),
                runtime=data.get("runtime"),
                rating=data.get("rating"),
                overview=data.get("overview")
            )

            movie = get_movie_by_title(data.get("title"))
            if movie:
                update_movie_status(movie[0], "want_to_watch")

            added += 1
            print(f"Added: {data.get('title')}")
        else:
            failed += 1
            print(f"Failed: {title}")

        time.sleep(delay)

    print(f"\nImport complete")
    print(f"Added: {added}")
    print(f"Failed: {failed}")